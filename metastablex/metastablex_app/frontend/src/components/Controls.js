export default function Controls({ws}){

  const send = (msg)=>{
    if(ws.current?.readyState===1){
      ws.current.send(JSON.stringify(msg));
    }
  };

  return(
    <div className="bg-white/5 p-4 rounded-xl border border-white/10 text-xs">

      <h2 className="mb-2">Controls</h2>

      <button onClick={()=>send({scenario:"low_noise"})}>
        Low Noise
      </button>

      <button onClick={()=>send({scenario:"critical"})}>
        Critical
      </button>

      <button onClick={()=>send({scenario:"chaotic"})}>
        Chaotic
      </button>

    </div>
  );
}
