import { Application } from "@/lib/application/use-cases";
import HttpAccountGateway from "./account/gateway";
import HttpAnalyticsGateway from "./analytics/gateway";
import { createWireClient } from "./api/wire-client";
import HttpAuthGateway from "./auth/gateway";
import HttpSpeechGateway from "./speech/gateway";

export default function composeApplication(): Application {
  const client = createWireClient();
  return new Application({
    authGateway: new HttpAuthGateway(client),
    accountGateway: new HttpAccountGateway(client),
    analyticsGateway: new HttpAnalyticsGateway(client),
    speechGateway: new HttpSpeechGateway(client),
  });
}
