<script lang="ts">
  import {
    createQuery,
    createMutation,
    useQueryClient,
  } from "@tanstack/svelte-query";
  import {
    getTodos,
    createTodo,
    updateTodo,
    deleteTodo,
    type Todo,
    checkboxTodo,
  } from "../lib/api";

  let editTitle = $state("");
  let editingId = $state();

  const qc = useQueryClient();

  let filter = $state<"filter" | "all" | "active" | "done">("filter");
  let newTitle = $state("");

  const statusParam = $derived(
    filter === "filter" ? undefined : filter === "done"
  );
  //get mutation
  const todosQuery = createQuery<Todo[]>(() => ({
    queryKey: ["todos", filter],
    queryFn: () => getTodos(statusParam),
  }));
  //create mutation
  const createMut = createMutation(() => ({
    mutationFn: (title: string) => createTodo({ title, status: false }),
    onSuccess: async () => {
      newTitle = "";
      await qc.invalidateQueries({ queryKey: ["todos"] });
    },
  }));
  //check done mutation
  const toggleMut = createMutation(() => ({
    mutationFn: (todo: Todo) => checkboxTodo(todo.id, { status: !todo.status }),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ["todos"] });
    },
  }));
  //edit mutation
  const editMut = createMutation(() => ({
    mutationFn: ({ id, title }: { id: number; title: string }) =>
      updateTodo(id, { title }),
    onSuccess: async () => {
      editTitle = "";
      editingId = null;
      await qc.invalidateQueries({ queryKey: ["todos"] });
    },
  }));
  //delete mutation
  const deleteMut = createMutation(() => ({
    mutationFn: (id: number) => deleteTodo(id),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ["todos"] });
    },
  }));
  //add func
  function add() {
    const title = newTitle.trim();
    if (!title) return;
    createMut.mutate(title);
  }
</script>

<div class=" bg-amber-100 h-screen">
  <div class="flex pb-5 justify-center text-xl font-bold items-center">
    Todo
  </div>
  <!--refresh-->
  <button
    class="bg-white px-2 rounded-lg cursor-pointer"
    onclick={() => todosQuery.refetch()}
    disabled={todosQuery.isFetching}
  >
    {todosQuery.isFetching ? "Refreshing..." : "Refresh"}
  </button>

  <!--create-->
  <div class="flex gap-2 justify-center items-center">
    <div>Create a list</div>
    <input
      class="flex p-2 rounded-lg border"
      placeholder="New todo..."
      bind:value={newTitle}
      onkeydown={(e) => e.key === "Enter" && add()}
    />
    <button
      class="bg-green-200 p-2 rounded-md cursor-pointer"
      onclick={add}
      disabled={createMut.isPending}
    >
      {createMut.isPending ? "Adding..." : "Add"}
    </button>
  </div>

  <!--dropdown filter-->
  <select class="border rounded-md m-5">
    <div class="flex gap-2">
      <option
        class="cursor-not-allowed"
        onclick={() => (filter = "filter")}
        disabled={filter === "filter"}
      >
        filter
      </option>
      <option
        class="cursor-pointer"
        onclick={() => (filter = "all")}
        disabled={filter === "all"}>All</option
      >

      <option
        class="cursor-pointer"
        onclick={() => (filter = "active")}
        disabled={filter === "active"}>Active</option
      >
      <option
        class="cursor-pointer"
        onclick={() => (filter = "done")}
        disabled={filter === "done"}>Done</option
      >
    </div>
  </select>

  {#if todosQuery.isError}
    <p class="bg-red-500">Error</p>
  {/if}

  {#if todosQuery.isLoading}
    <p>Loading...</p>
  {:else}
    <ul>
      {#each todosQuery.data ?? [] as list (list.id)}
        <li class="flex justify-between items-center p-5 border-b">
          <div class="flex gap-5 items-center;">
            <input
              class="w-5 h-5"
              type="checkbox"
              checked={list.status}
              onchange={() => toggleMut.mutate(list)}
              disabled={toggleMut.isPending}
            />
            {#if editingId !== list.id}
              <span class={list.status ? "text-red-400 line-through" : ""}>
                list {list.id}:
                {list.title}
              </span>
            {:else}
              <input class="border focus:ring" bind:value={editTitle} />
            {/if}
          </div>
          {#if editingId !== list.id}
            <div class="flex justify-around gap-2">
              <!--update-->
              <button
                class="bg-blue-200 rounded-md px-2 cursor-pointer"
                onclick={() => {
                  ((editTitle = list.title), (editingId = list.id));
                }}
              >
                Edit
              </button>

              <!--delete-->
              <button
                class="bg-red-200 rounded-md px-2 cursor-pointer"
                onclick={() => deleteMut.mutate(list.id)}
                disabled={deleteMut.isPending}
              >
                Delete
              </button>
            </div>
          {:else}
            <div class="flex justify-around gap-2">
              <!--save-->
              <button
                onclick={() =>
                  editMut.mutate({ id: list.id, title: editTitle })}
                disabled={editMut.isPending || !editTitle.trim()}
                onkeydown={(e) =>
                  e.key === "Enter" &&
                  editMut.mutate({ id: list.id, title: editTitle })}
                class="bg-green-200 rounded-md cursor-pointer px-2">Save</button
              >
              <!--cancel-->
              <button
                onclick={() => (editingId = null)}
                class="bg-red-200 rounded-md cursor-pointer px-2">Cancel</button
              >
            </div>
          {/if}
        </li>
      {/each}
    </ul>
  {/if}
</div>
