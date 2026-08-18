import createClient, { type Client, type Middleware } from "openapi-fetch";

import type { paths } from "./generated/schema";
import { NetworkError } from "./errors";

export type ApiWireClient = Client<paths>;

export function createWireClient(): ApiWireClient {
  const client = createClient<paths>({ credentials: "same-origin" });
  const middleware: Middleware = {
    onError({ error }) {
      return new NetworkError({ cause: error });
    },
  };
  client.use(middleware);
  return client;
}
