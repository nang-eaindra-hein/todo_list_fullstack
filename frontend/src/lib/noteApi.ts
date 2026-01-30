export type Note = { id: number; des: string };
export type NoteCreate = { des: string};

import { PUBLIC_API_URL } from '$env/static/public';


//get
export async function getNotes(todoId:number): Promise<Note[]> {
    const url =`${PUBLIC_API_URL}/todo/${todoId}/note`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to load notes");
  return res.json();
}
//create
export async function createNote(todoId:number,data: NoteCreate): Promise<Note> {
  const res = await fetch(`${PUBLIC_API_URL}/todo/${todoId}/note`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...data })
  });
  if (!res.ok) throw new Error("Failed to create note");
  return res.json();
}

//put(update)
export function updateNote(todoId: number,note_id:number, payload: { des: string }) {
  return fetch(`${PUBLIC_API_URL}/todo/${todoId}/note/${note_id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  }).then(r => r.json());
}

//delete
export async function deleteNote(todoId: number,note_id:number): Promise<void> {
  const res = await fetch(`${PUBLIC_API_URL}/todo/${todoId}/note/${note_id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete todo");
  
}
