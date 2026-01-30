<script lang="ts">
  import { createMutation, useQueryClient } from "@tanstack/svelte-query";
  import { goto } from "$app/navigation";

  import { createNote } from "$lib/noteApi";
  import NoteList from "$lib/components/NoteList.svelte";
  import Button from "$lib/components/Button.svelte";
  let notes = $state("");
  import { page } from "$app/stores";
  import { get } from "svelte/store";
  import { SvelteDate } from "svelte/reactivity";
  let { date, lastSavedAt }: { date: any; lastSavedAt: any } = $props();
  const todoId = Number(get(page).params.todoId);

  const qc = useQueryClient();
  //create mutation

  const createMut = createMutation(() => ({
    mutationFn: ({ todoId, des }: { todoId: number; des: string }) =>
      createNote(todoId, { des }),
    onSuccess: async () => {
      notes = "";
      await qc.invalidateQueries({ queryKey: ["Notes"] });
    },
  }));

  //add func
  function addNote(todoId: number) {
    const des = notes.trim();
    if (!des) return;
    createMut.mutate({ todoId, des });
  }
  //back btn
  function goBack() {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      goto("/");
    }
  }
</script>

<div class="bg-amber-100 h-screen">
  <h1
    class="text-purple-900 justify-center flex text-2xl pb-5 underline font-bold"
  >
    Notes
  </h1>

  <Button onclick={goBack} variant="Blue">back</Button>

  <div>
    <textarea
      placeholder="write your notes..."
      class="border p-10 m-10 rounded-xl text-amber-950"
      bind:value={notes}
      onkeydown={(e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          addNote(todoId);
        }
      }}
    ></textarea>

    <Button
      onclick={() => {
        addNote(todoId);
        date = new SvelteDate();
        lastSavedAt = new Date();
      }}
      variant="Green">put</Button
    >
  </div>

  <!--note lists-->
  <NoteList {todoId} {qc} />
</div>
