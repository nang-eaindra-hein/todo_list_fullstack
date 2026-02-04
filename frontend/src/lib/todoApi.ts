export type Todo = { id: number; title: string; status: boolean};
export type TodoCreate = { title: string; status?: boolean };
export type TodoUpdate = { title?: string; status?: boolean };
import { PUBLIC_API_URL } from '$env/static/public';


//get
export async function getTodos(status?: boolean): Promise<Todo[]> {
    const url =
    status === undefined
      ?  `${PUBLIC_API_URL}/todo`
      : `${PUBLIC_API_URL}/todo?status=${status}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to load todos");
  const todos = await res.json();
  return todos;
  
}

//create
export async function createTodo(data: TodoCreate): Promise<Todo> {
  const res = await fetch(`${PUBLIC_API_URL}/todo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({   title: data.title,
      status: data.status ?? false,
      })
  });
  if (!res.ok) throw new Error("Failed to create todo");
  
  const todo = await res.json();
  return todo;
}

//put(checkbox)
export async function checkboxTodo(id: number, data: TodoUpdate): Promise<Todo> {
  const res = await fetch (`${PUBLIC_API_URL}/todo/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error("Failed to update todo");
  return res.json();
}
//put(update)
export function updateTodo(id: number, payload: { title: string }) {
  return fetch(`${PUBLIC_API_URL}/todo/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  }).then(r => r.json());
}

//delete
export async function deleteTodo(id: number): Promise<void> {
  const res = await fetch(`${PUBLIC_API_URL}/todo/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete todo");
  
}
