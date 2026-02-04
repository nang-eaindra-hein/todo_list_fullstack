<script lang="ts">
  import {
    createQuery,
    createMutation,
    useQueryClient,
  } from "@tanstack/svelte-query";
  import { toast, Toaster } from "svelte-french-toast";

  import { getTodos, createTodo, type Todo } from "$lib/todoApi";
  import Lists from "$lib/components/Lists.svelte";
  import Button from "$lib/components/Button.svelte";
  import Dark from "$lib/components/Dark.svelte";

  let newTitle = $state("");
  const qc = useQueryClient();
  //filter
  let filter = $state<"Filter" | "All" | "Checked" | "Unchecked">("Filter");

  const statusParam = $derived(
    filter === "Checked" ? true : filter === "Unchecked" ? false : undefined
  );

  //add func
  function add() {
    const title = newTitle.trim();
    if (!title) return;
    createMut.mutate(title);
    toast.success("Added todo list!");
  }
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
</script>

<div class=" bg-amber-100 h-screen">
  <div
    class="underline text-purple-900 flex pb-5 justify-center text-xl font-bold items-center"
  >
    Todo List
  </div>
  <!--refresh-->
  <Button
    variant="Blue"
    onclick={() => todosQuery.refetch()}
    disabled={todosQuery.isFetching}
  >
    {todosQuery.isFetching ? "Refreshing..." : "Refresh"}
  </Button>
  <Dark />
  <!--create-->
  <div class="flex gap-2 justify-center items-center">
    <div>Create a list</div>
    <input
      class="flex p-2 rounded-lg border"
      placeholder="New todo..."
      bind:value={newTitle}
      onkeydown={(e) => e.key === "Enter" && add()}
    />
    <Button variant="Green" onclick={add} disabled={createMut.isPending}>
      {createMut.isPending ? "Adding..." : "Add"}
    </Button>
  </div>

  <!--dropdown filter-->

  <select
    bind:value={filter}
    class="rounded shadow-md texts-sm ml-5 cursor-pointer bg-amber-50"
  >
    <option value="Filter" selected disabled>Filter</option>
    <option value="All">All</option>
    <option value="Checked">Checked</option>
    <option value="Unchecked">Unchecked</option>
  </select>
  <!--lists-->
  <Lists {qc} {todosQuery} />
</div>
<Toaster />
