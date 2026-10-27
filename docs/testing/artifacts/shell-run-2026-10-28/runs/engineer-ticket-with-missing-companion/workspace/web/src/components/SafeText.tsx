import { tokenise } from "../lib/safe-content";

// Renders untrusted model text. No dangerouslySetInnerHTML: React escapes every text node.
export function SafeText({ source }: { source: string }) {
  return (
    <>
      {tokenise(source).map((token, i) => {
        if (token.kind === "text") return <span key={i}>{token.text}</span>;
        if (token.kind === "link") {
          return (
            <a key={i} href={token.href} target="_blank" rel="noopener noreferrer nofollow">
              {token.label}
            </a>
          );
        }
        return <img key={i} src={token.src} alt={token.alt} referrerPolicy="no-referrer" />;
      })}
    </>
  );
}
