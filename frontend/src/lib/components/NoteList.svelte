<script lang="ts">
  import Button from "./Button.svelte";
  import { SvelteDate } from "svelte/reactivity";
  import { createMutation, createQuery } from "@tanstack/svelte-query";
  let { todoId, qc }: { todoId: number; qc: any } = $props();
  import { getNotes, updateNote, deleteNote, type Note } from "$lib/noteApi";
  let editDes = $state("");
  let editingId = $state();

  //date time
  let lastSavedAt = $state<Date | null>(null);
  let date = $state(new SvelteDate());
  let currentDate = $derived(
    date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    })
  );
  let currentHour = $derived(
    date.toLocaleTimeString(undefined, {
      hour: "numeric",
    })
  );
  let currentMin = $derived(
    date.toLocaleTimeString(undefined, {
      minute: "numeric",
    })
  );

  //get mutation
  const notesQuery = createQuery<Note[]>(() => ({
    queryKey: ["Notes"],
    queryFn: () => getNotes(todoId),
  }));

  //edit mutation

  const editMut = createMutation(() => ({
    mutationFn: ({
      todoId,
      noteId,
      des,
    }: {
      todoId: number;
      noteId: number;
      des: string;
    }) => updateNote(todoId, noteId, { des }),
    onSuccess: async () => {
      editDes = "";
      editingId = null;

      await qc.invalidateQueries({ queryKey: ["Notes"] });
    },
  }));
  //delete mutation
  const deleteMut = createMutation(() => ({
    mutationFn: ({ id, note_id }: { id: number; note_id: number }) =>
      deleteNote(id, note_id),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ["Notes"] });
    },
  }));
</script>

{#if notesQuery.isError}
  <p class="bg-red-500">Error</p>
{/if}

{#if notesQuery.isLoading}
  <p>Loading...</p>
{:else}
  <ul>
    {#each notesQuery.data ?? [] as note (note.id)}
      <li class="flex justify-between items-start p-5 border-b">
        <div class="flex gap-5 items-cente w-full">
          {#if editingId !== note.id}
            <div class="justify-start flex">
              <span class="min-w-15"> note {note.id}:</span>
              <span>{note.des}</span>
            </div>
          {:else}
            <textarea
              class="border focus:ring rounded-lg px-2 w-full"
              bind:value={editDes}
            >
            </textarea>
          {/if}
        </div>
        {#if editingId !== note.id}
          <div class="flex justify-end gap-2">
            <div class="pr-5 text-nowrap">
              Noted: {currentDate}, {currentHour}:{currentMin}
            </div>
            <Button
              variant="Blue"
              onclick={() => {
                ((editDes = note.des), (editingId = note.id));
              }}
            >
              Edit
            </Button>

            <Button
              onclick={() => deleteMut.mutate({ id: todoId, note_id: note.id })}
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
                date = new SvelteDate();
                lastSavedAt = new Date();

                editMut.mutate({
                  todoId: todoId,
                  noteId: note.id,
                  des: editDes,
                });
              }}
              disabled={editMut.isPending || !editDes.trim()}
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
