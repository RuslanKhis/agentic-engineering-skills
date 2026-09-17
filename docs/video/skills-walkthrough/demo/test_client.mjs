import {test} from 'node:test';
import assert from 'node:assert/strict';
import {streamReply} from './client.js';
const encoder = new TextEncoder();
function mockStream(chunks) {
  let request;
  globalThis.fetch = async (url, options) => {
    request = {url, options};
    return new Response(new ReadableStream({start(controller) {
      for (const chunk of chunks)
        controller.enqueue(typeof chunk === 'string' ? encoder.encode(chunk) : chunk);
      controller.close();
    }}));
  };
  return () => request;
}
async function run(chunks) {
  mockStream(chunks);
  const events = [];
  await streamReply({message:'Hi', sessionId:null, token:'demo-alice', onEvent:e=>events.push(e)});
  return events;
}
test('UTF-8 text and NDJSON lines survive chunk boundaries', async () => {
  const data = encoder.encode('{"type":"text","text":"Español"}\n{"type":"done"}\n');
  const split = data.indexOf(0xc3) + 1;
  const events = await run([data.slice(0, 9), data.slice(9, split), data.slice(split)]);
  assert.equal(events[0].text, 'Español');
  assert.equal(events[1].type, 'done');
});
test('auth travels in header, owner cannot be supplied in body', async () => {
  const request = mockStream(['{"type":"done"}\n']);
  await streamReply({message:'Hi', sessionId:null, token:'demo-alice', onEvent(){}});
  assert.equal(request().options.headers.Authorization, 'Bearer demo-alice');
  assert.deepEqual(JSON.parse(request().options.body), {message:'Hi',session_id:null});
});
test('missing terminal frame rejects an interrupted stream', async () => {
  await assert.rejects(run(['{"type":"text","text":"Hello"}\n']), /interrupted/);
});
test('malformed public event is rejected', async () => {
  await assert.rejects(run(['{"type":"text","text":42}\n']), /Invalid/);
});
test('late error remains terminal, not success', async () => {
  const events = await run(['{"type":"text","text":"Hello"}\n{"type":"error","message":"Failed"}\n']);
  assert.equal(events.at(-1).type, 'error');
  assert.ok(!events.some(e=>e.type==='done'));
});
test('event after terminal rejects invalid ordering', async () => {
  await assert.rejects(run(['{"type":"done"}\n{"type":"text","text":"Late"}\n']), /Invalid/);
});
