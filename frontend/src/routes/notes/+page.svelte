<script>
    import { onMount } from 'svelte';
    import Tiptap from '$lib/Tiptap.svelte'

    import { writable } from 'svelte/store';



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




	// export let accounts: Account[];
	// export let mails: Mail[];

    // export const mails = [
	// {
	// 	id: "6c84fb90-12c4-11e1-840d-7b25c5ee775a",
	// 	title: "Shopping List",
	// 	email: "williamsmith@example.com",
	// 	content: "Hi, let's have a meeting tomorrow to discuss the project. I've been reviewing the project details and have some ideas I'd like to share. It's crucial that we align on our next steps to ensure the project's success.\n\nPlease come prepared with any questions or insights you may have. Looking forward to our meeting!\n\nBest regards, William",
	// 	created_at: "2023-10-22T09:00:00",
    //     updated_at: "2023-10-22T09:00:00",
    //     remind_at: "2023-10-22T10:30:00",
	//     },
    //     {
	// 	id: "110e8400-e29b-11d4-a716-446655440000",
	// 	title: "Alice Smith",
	// 	email: "alicesmith@example.com",
	// 	content: "Thank you for the project update. It looks great! I've gone through the report, and the progress is impressive. The team has done a fantastic job, and I appreciate the hard work everyone has put in.\n\nI have a few minor suggestions that I'll include in the attached document.\n\nLet's discuss these during our next meeting. Keep up the excellent work!\n\nBest regards, Alice",
	// 	created_at: "2023-10-22T09:00:00",
    //     updated_at: "2023-10-22T09:00:00",
    //     remind_at: "2023-10-22T10:30:00",
	// }
    // ]


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

                    <!-- if selected add bg-muted else Not in that button class -->
                    <!-- <button class="hover:bg-accent flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all bg-muted" on:click={() => mailStore.setMail(item.id)}> -->
                    <ScrollArea class="h-screen">
                        <div class="flex flex-col gap-2 p-4 pt-0">
                            {#each mails as item}
                                <button class="hover:bg-accent flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all" on:click={() => selectMail(item.id) }>
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
				<Tabs.Content value="unread" class="m-0">
					<!-- <MailList items={mails.filter((item) => !item.read)} /> -->
				</Tabs.Content>
			</Tabs.Root>
		</Resizable.Pane>

        <!--Display note component seperate from here -->
		<Resizable.Handle withHandle />
		<Resizable.Pane defaultSize={defaultLayout[2]}>
			<!-- <MailDisplay mail={mails.find((item) => item.id === $mailStore.selected) || null} /> -->








            <div class="flex h-full flex-col">
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

                        <Separator orientation="vertical" class="mx-1 h-6" />

                        <!-- <Tooltip.Root openDelay={0} group>
                            <Popover.Root portal={null}>
                                <Tooltip.Trigger asChild let:builder={tooltip_builder} id="snooze_popover">
                                    <Popover.Trigger asChild let:builder={popover_builder} id="snooze_popover">
                                        <Button
                                            builders={[tooltip_builder, popover_builder]}
                                            variant="ghost"
                                            size="icon"
\                                        >
                                            <Icons.Clock class="size-4" />
                                            <span class="sr-only">Remind me</span>
                                        </Button>
                                    </Popover.Trigger>
                                </Tooltip.Trigger>

                                <Popover.Content class="flex w-[535px] p-0">
                                    <div class="flex flex-col gap-2 border-r px-2 py-4">
                                        <div class="px-4 text-sm font-medium">Snooze until</div>
                                        <div class="grid min-w-[250px] gap-1">
                                            <Button variant="ghost" class="justify-start font-normal">
                                                Later today
                                                <span class="text-muted-foreground ml-auto">
                                                    {relativeFormatter.format(
                                                        todayDate.add({ hours: 4 }).toDate()
                                                    )}
                                                </span>
                                            </Button>
                                            <Button variant="ghost" class="justify-start font-normal">
                                                Tomorrow
                                                <span class="text-muted-foreground ml-auto">
                                                    {relativeFormatter.format(
                                                        todayDate.add({ days: 1 }).toDate()
                                                    )}
                                                </span>
                                            </Button>
                                            <Button variant="ghost" class="justify-start font-normal">
                                                This weekend
                                                <span class="text-muted-foreground ml-auto">
                                                    {relativeFormatter.format(getClosestWeekend())}
                                                </span>
                                            </Button>
                                            <Button variant="ghost" class="justify-start font-normal">
                                                Next week
                                                <span class="text-muted-foreground ml-auto">
                                                    {relativeFormatter.format(
                                                        todayDate.add({ weeks: 1 }).toDate()
                                                    )}
                                                </span>
                                            </Button>
                                        </div>
                                    </div>
                                    <div class="p-2">
                                        <Calendar bind:value={todayDate} initialFocus />
                                    </div>
                                </Popover.Content>
                            </Popover.Root>
                            <Tooltip.Content>Snooze</Tooltip.Content>
                        </Tooltip.Root> -->


                    </div>
                    <div class="ml-auto flex items-center gap-2">
                        Loader here
                    </div>
                    <Separator orientation="vertical" class="mx-2 h-6" />
                </div>
                <Separator />
                {#if selectedNote}
                    <div class="flex h-full flex-1 flex-col overflow-hidden">
                        <div class="flex items-start p-4">
                            <div class="flex items-start gap-4 text-sm">
                                <div class="grid gap-1">
                                    <!-- <div class="font-semibold">Alison Smith</div> -->
                                    <h4 class="scroll-m-20 text-2xl font-semibold tracking-tight">
                                        {selectedNote ? selectedNote.title : 'Select a note'} 
                                    </h4>
                                </div>
                            </div>
                            <div class="text-muted-foreground ml-auto text-xs">
                                Updated: { selectedNote.updated_at_readable }
                            </div>
                        </div>

                        <div class="flex-1 overflow-y-auto whitespace-pre-wrap p-4 text-sm">
                            <Tiptap />
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