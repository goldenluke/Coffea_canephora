export const WS_URL =
  window.location.hostname.includes("ngrok")
    ? "wss://metastablex.ngrok-free.app/ws/qwan/"
    : "ws://127.0.0.1:8000/ws/qwan/";
