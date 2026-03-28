export default function ReplayControls({ ws }) {

  const send = (msg) => {
    if (ws && ws.readyState === 1) {
      ws.send(JSON.stringify(msg));
    }
  };

  return (
    <div className="flex gap-2 text-xs mt-2">

      <button onClick={()=>send({mode:"live"})}>
        LIVE
      </button>

      <button onClick={()=>send({mode:"replay", index:0})}>
        ⏪
      </button>

      <button onClick={()=>send({mode:"replay", index:50})}>
        ⏩
      </button>

    </div>
  );
}
