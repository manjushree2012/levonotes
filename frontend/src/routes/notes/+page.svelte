<script>
    import { onMount } from 'svelte';
    import Tiptap from '$lib/Tiptap.svelte'

    import { writable } from 'svelte/store';
    import { DateInput } from 'date-picker-svelte'

    let reminderDateTime = new Date()




    let mails = [];
    let loading = true;
    let error = null;

    const selectedNoteId = writable(null)

    onMount(async () => {
        try {
        const response = await fetch('http://127.0.0.1:5000/notes');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        mails = await response.json();
        } catch (e) {
        error = e.message;
        } finally {
        loading = false;
        }
    });




	import Search from "lucide-svelte/icons/search";
	// import { primaryRoutes, secondaryRoutes } from "../config.js";
	// import { mailStore } from "../store.js";
	// import type { Account, Mail } from "../data.js";
	// import AccountSwitcher from "./account-switcher.svelte";
	// import MailDisplay from "./mail-display.svelte";
	// import MailList from "./mail-list.svelte";
	// import Nav from "./nav.svelte";
	import { cn } from "$lib/utils.js";

    import * as Resizable from "$lib/components/ui/resizable";
    import { Separator } from "$lib/components/ui/separator";
    import * as Tabs from "$lib/components/ui/tabs";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import { Badge } from "$lib/components/ui/badge";

    import * as Tooltip from "$lib/components/ui/tooltip";
    import { Button, buttonVariants } from "$lib/components/ui/button";

    import { Trash2 } from 'lucide-svelte';
    import { AlarmClock } from 'lucide-svelte';

    import { NotebookPen } from 'lucide-svelte';

	export let defaultLayout = [265, 440, 655];
	export let defaultCollapsed = false;
	// export let navCollapsedSize: number;

	let isCollapsed = defaultCollapsed;

    function get_badge_variant_from_label(label) {
		if (["work"].includes(label.toLowerCase())) {
			return "default";
		}

		if (["personal"].includes(label.toLowerCase())) {
			return "outline";
		}

		return "secondary";
	}

	function onLayoutChange(sizes) {
		document.cookie = `PaneForge:layout=${JSON.stringify(sizes)}`;
	}

	function onCollapse() {
		isCollapsed = true;
		document.cookie = `PaneForge:collapsed=${true}`;
	}

	function onExpand() {
		isCollapsed = false;
		document.cookie = `PaneForge:collapsed=${false}`;
	}

    function selectMail(id) {
        selectedNoteId.set(id);
    }

    // Reactive variable to get the selected note object
    $: selectedNote = mails.find(mail => mail.id === $selectedNoteId);

    // Reactive statement to call the API when the date changes
    $: {
        updateDateAPI(reminderDateTime);
    }

    async function updateDateAPI(newDate) {
        console.log('Reminder changed')

        try {
            const response = await fetch('http://your-api-endpoint.com/update-date', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ date: newDate }),
            });

            if (!response.ok) {
                throw new Error('Failed to update date');
            }

            const result = await response.json();
            console.log('Date updated successfully:', result);
        } catch (error) {
            console.error('Error updating date:', error);
        }

    }
</script>

<div class="hidden md:block">
	<Resizable.PaneGroup
		direction="horizontal"
		{onLayoutChange}
		class="h-full max-h-[800px] items-stretch"
	>		
		<Resizable.Handle withHandle />
		<Resizable.Pane defaultSize={defaultLayout[1]} minSize={30}>
			<Tabs.Root value="all">
				<div class="flex items-center px-4 py-2">
					<h1 class="text-xl font-bold">All notes</h1>
                    <Button class="ml-auto">
                        <!-- <EnvelopeOpen class="mr-2 h-4 w-4" /> -->
                        <NotebookPen  class="mr-2 h-4 w-4" />
                        Create New
                      </Button>
				</div>
                
				<Separator />
				
				<Tabs.Content value="all" class="m-0">
                    <!-- Notes List Start -->

                    <ScrollArea class="h-screen">
                        <div class="flex flex-col gap-2 p-4 pt-0">
                            {#each mails as item}
                                <button 
                                class={`hover:bg-accent flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all ${$selectedNoteId === item.id ? 'bg-muted' : ''}`} 
                                on:click={() => selectMail(item.id) }>
                                    <div class="flex w-full flex-col gap-1">
                                        <div class="flex items-center">
                                            <div class="flex items-center gap-2">
                                                <span class="flex h-2 w-2 rounded-full bg-blue-600" />
                                                <div class="font-semibold">{item.title}</div>
                                            </div>

                                            <!-- ml-auto text-xs text-muted-foreground -->
                                             <!-- Add this class if selcted or smething for time wala class -->
                                            <div class="ml-auto text-xs text-foreground">
                                                { item.updated_at_readable }
                                            </div>
                                        </div>
                                    </div>
                                    <div class="text-muted-foreground line-clamp-2 text-xs">
                                        {item.content.substring(0, 300)}
                                    </div>
                                    {#if item.reminder}
                                        <div class="flex items-center gap-2">
                                            <Badge> Remind me:  {item.reminder.reminder_time_readable} </Badge>
                                        </div>
                                    {/if }
                                </button>
                            {/each}
                        </div>
                    </ScrollArea>
				</Tabs.Content>
			</Tabs.Root>
		</Resizable.Pane>

        <!--Display note component seperate from here -->
		<Resizable.Handle withHandle />
		<Resizable.Pane defaultSize={defaultLayout[2]}>
            <div class="flex h-full flex-col">
                {#if selectedNote}
                    <div class="mb-1 flex items-center p-2">
                        <div class="flex items-center gap-2">
                            <Tooltip.Root openDelay={0} group>
                                <Tooltip.Trigger
                                    id="move_to_trash_tooltip"
                                    class={buttonVariants({ variant: "ghost", size: "icon" })}>
                                    <Trash2 />
                                    <span class="sr-only">Move to trash</span>
                                </Tooltip.Trigger>
                                <Tooltip.Content>Move to trash</Tooltip.Content>
                            </Tooltip.Root>

                            <DateInput 
                                bind:value={reminderDateTime}
                                timePrecision="minute"                            
                            />
                            <Separator orientation="vertical" class="mx-1 h-6" />
                        </div>
                        <div class="ml-auto flex items-center gap-2">
                            Loader here
                        </div>
                        <Separator orientation="vertical" class="mx-2 h-6" />
                    </div>
                {/if}
                <Separator />
                {#if selectedNote}
                    <div class="flex h-full flex-1 flex-col overflow-hidden">
                        <div class="flex items-start p-4">
                            <div class="flex items-start gap-4 text-sm">
                                <div class="grid gap-1">
                                    <h4 class="scroll-m-20 text-2xl font-semibold tracking-tight">
                                        {selectedNote.title } 
                                    </h4>
                                </div>
                            </div>
                            <div class="text-muted-foreground ml-auto text-xs">
                                Updated: { selectedNote.updated_at_readable }
                            </div>
                        </div>

                        <div class="flex-1 overflow-y-auto whitespace-pre-wrap p-4 text-sm">
                            {selectedNote.content}
                            <Tiptap content={selectedNote.content} />
                        </div>
                        <Separator class="mt-auto" />
                    </div>
                {:else}
                    <div class="text-muted-foreground p-8 text-center">No note has been selected.</div>
                {/if}
            </div>
		</Resizable.Pane>
	</Resizable.PaneGroup>
</div>