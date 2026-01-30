<script lang="ts">
  import Button from "$lib/components/Button.svelte";
  import {
    createQuery,
    createMutation,
    useQueryClient,
  } from "@tanstack/svelte-query";

  import {
    getTodos,
    checkboxTodo,
    updateTodo,
    deleteTodo,
    type Todo,
  } from "$lib/todoApi";
  let { qc, todosQuery }: { qc: any; todosQuery: any } = $props();

  let editTitle = $state("");
  let editingId = $state();

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
</script>

{#if todosQuery.isError}
  <p class="bg-red-500">Error</p>
{/if}

{#if todosQuery.isLoading}
  <p>Loading...</p>
{:else}
  <ul>
    {#each todosQuery.data ?? [] as list (list.id)}
      <li class="flex justify-between items-center p-5 border-b">
        <div class="flex gap-5 items-center">
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
            <input
              class="border focus:ring rounded-lg px-2"
              bind:value={editTitle}
            />
          {/if}
        </div>
        {#if editingId !== list.id}
          <div class="flex justify-around gap-2">
            <a
              href="/todo/{list.id}/note"
              class="bg-purple-200 rounded-md px-2 cursor-pointer">See Note</a
            >

            <Button
              variant="Blue"
              onclick={() => {
                ((editTitle = list.title), (editingId = list.id));
              }}
            >
              Edit
            </Button>

            <Button
              onclick={() => deleteMut.mutate(list.id)}
              disabled={deleteMut.isPending}
              variant="Red"
            >
              Delete
            </Button>
          </div>
        {:else}
          <div class="flex justify-around gap-2">
            <!--save-->
            <Button
              onclick={() => editMut.mutate({ id: list.id, title: editTitle })}
              disabled={editMut.isPending || !editTitle.trim()}
              variant="Green">Save</Button
            >
            <!--cancel-->
            <Button onclick={() => (editingId = null)} variant="Red"
              >Cancel
            </Button>
          </div>
        {/if}
      </li>
    {/each}
  </ul>
{/if}
