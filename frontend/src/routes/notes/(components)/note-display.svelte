<script>
    import { DateInput } from 'date-picker-svelte';
    import { Input } from "$lib/components/ui/input";
    import { Button } from "$lib/components/ui/button";
    import Reload from "svelte-radix/Reload.svelte";
    import { Trash2 } from 'lucide-svelte';
    import Tiptap from '$lib/Tiptap.svelte';
    import { BellPlus } from 'lucide-svelte';
    import { Separator } from "$lib/components/ui/separator";

    export let selectedNote;
    export let reminderDateTime;
    export let remind_mail;
    export let isLoading;
    export let updateDateAPI;
    export let deleteNote;
    export let handleContentUpdate;
</script>

<div class="flex h-full flex-col">
    {#if selectedNote}
        <div class="mb-1 flex items-center p-2">
            <div class="flex items-center gap-2">
                <DateInput 
                    bind:value={reminderDateTime}
                    timePrecision="minute"      
                    min={new Date()}  
                    placeholder="Pick a future datetime"                    
                />
                to 
                <Input
                    type="email"
                    placeholder="Email address"
                    class="pl-8"
                    bind:value={remind_mail} 
                />
                <Button variant="outline" on:click={updateDateAPI}>
                    <BellPlus class="mr-2 h-4 w-4" />
                </Button>
            </div>
            <div class="ml-auto flex items-center gap-2">
                {#if isLoading}
                    <Reload class="mr-2 h-4 w-4 animate-spin" />
                {/if}
                <Button 
                    class="ml-auto"
                    variant="destructive"
                    on:click={deleteNote}>
                    <Trash2 class="mr-2 h-4 w-4"/>
                </Button>
            </div>
        </div>
        <Separator />
        <div class="flex-1 overflow-y-auto whitespace-pre-wrap p-4 text-sm">
            <Tiptap content={selectedNote.content} on:contentUpdated={handleContentUpdate} />
        </div>
    {:else}
        <div class="text-muted-foreground p-8 text-center">No note has been selected.</div>
    {/if}
</div>