export default function Field({field}){

  if(!field) return <div>Loading...</div>;

  return(
    <div style={{
      display:"grid",
      gridTemplateColumns:`repeat(${field.length},3px)`
    }}>
      {field.flat().map((v,i)=>{

        const energy = v*v;

        return(
          <div key={i}
            style={{
              width:3,
              height:3,
              background:`hsl(${energy*240},100%,60%)`
            }}
          />
        )
      })}
    </div>
  );
}
