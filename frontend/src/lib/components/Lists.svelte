<script lang="ts">
  import Button from "$lib/components/Button.svelte";
  import { createMutation } from "@tanstack/svelte-query";
  import {
    checkboxTodo,
    updateTodo,
    deleteTodo,
    type Todo,
  } from "$lib/todoApi";

  import { toast, Toaster } from "svelte-french-toast";
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
  //draggable
  let mouseYCoordinate = null;
  let distanceTopGrabbedVsPointer = null;

  let draggingItem = null;
  let draggingItemId = null;
  let draggingItemIndex: any = null;

  let hoveredItemIndex = null;

  if (mouseYCoordinate == null || mouseYCoordinate == 0) {
    // showGhost = false;
  }

  if (
    draggingItemIndex != null &&
    hoveredItemIndex != null &&
    draggingItemIndex != hoveredItemIndex
  ) {
    // swap items
    [todosQuery.data[draggingItemIndex], todosQuery.data[hoveredItemIndex]] = [
      todosQuery.data[hoveredItemIndex],
      todosQuery.data[draggingItemIndex],
    ];

    // balance
    draggingItemIndex = hoveredItemIndex;
  }

  let container = null;
</script>

{#if todosQuery.isError}
  <p class="bg-red-500">Error</p>
{/if}

{#if todosQuery.isLoading}
  <p>Loading...</p>
{:else}
  <ul>
    {#each todosQuery.data ?? [] as list (list.id)}
      <li class="expandable flex justify-between items-center p-5 border-b">
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
            <div class="pr-5 text-nowrap">
              <!--datetime-->
              Updated: {list.updated_at}
            </div>

            <!--draw note-->
            <a
              href="/todo/{list.id}/draw"
              class="bg-purple-200 rounded-md px-2 cursor-pointer">Draw Note</a
            >
            <!--see note-->
            <a
              href="/todo/{list.id}/note"
              class="bg-purple-200 rounded-md px-2 cursor-pointer"
              >See Note<!--total-->
              {#if list.note_count > 0}
                <span class="rounded-lg px-2 bg-blue-200 text-xs"
                  >{list.note_count}</span
                >
              {/if}</a
            >
            <!--draggable-->
            <Button variant="Blue" class="draggable">Drag</Button>
            <!--edit btn-->

            <Button
              variant="Blue"
              onclick={() => {
                ((editTitle = list.title), (editingId = list.id));
              }}
            >
              Edit
            </Button>
            <!--delete btn-->
            <Button
              onclick={() => {
                deleteMut.mutate(list.id);
                toast.success("Deleted Todo list!");
              }}
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
              onclick={() => {
                editMut.mutate({ id: list.id, title: editTitle });
                toast.success("Saved Editing!");
              }}
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
<Toaster />
