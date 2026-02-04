export type Draw = { id: number; img: string};
export type drawCreate = { img: string};


import { PUBLIC_API_URL } from '$env/static/public';


//get
export async function getDraw(todoId:number): Promise<Draw[]> {
    const url =`${PUBLIC_API_URL}/todo/${todoId}/draw`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to load draws");
  return res.json();
}

//create
export async function createDraw(todoId:number,data: drawCreate): Promise<Draw> {
  const res = await fetch(`${PUBLIC_API_URL}/todo/${todoId}/draw`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...data })
  });
  if (!res.ok) throw new Error("Failed to create draw");
  return res.json();
}

