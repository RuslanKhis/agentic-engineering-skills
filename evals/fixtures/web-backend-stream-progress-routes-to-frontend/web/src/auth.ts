import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseApp = initializeApp({
  apiKey: import.meta.env.VITE_IDP_API_KEY,
  authDomain: import.meta.env.VITE_IDP_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_IDP_PROJECT_ID,
});

export const auth = getAuth(firebaseApp);

export async function getIdToken(): Promise<string> {
  const user = auth.currentUser;
  if (!user) throw new Error("not signed in");
  return user.getIdToken();
}
