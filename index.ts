import * as express from "express";
import { resolve } from "path";
const app = express();

// get port and hostname from environment variables, or use defaults if not set
const PORT = process.env.NODE_PORT ?? "3000";
const HOSTNAME = process.env.NODE_HOSTNAME ?? "localhost";

// directory to serve static content from
app.use(express.static(resolve(__dirname, "static")));

// start the server
app.listen(+PORT, HOSTNAME, () => {
  console.log(`Started server listening on ${HOSTNAME}:${PORT}...`);
});
