<script>
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

	// export let accounts: Account[];
	// export let mails: Mail[];

    export const mails = [
	{
		id: "6c84fb90-12c4-11e1-840d-7b25c5ee775a",
		title: "Shopping List",
		email: "williamsmith@example.com",
		content: "Hi, let's have a meeting tomorrow to discuss the project. I've been reviewing the project details and have some ideas I'd like to share. It's crucial that we align on our next steps to ensure the project's success.\n\nPlease come prepared with any questions or insights you may have. Looking forward to our meeting!\n\nBest regards, William",
		created_at: "2023-10-22T09:00:00",
        updated_at: "2023-10-22T09:00:00",
        remind_at: "2023-10-22T10:30:00",
	    },
        {
		id: "110e8400-e29b-11d4-a716-446655440000",
		title: "Alice Smith",
		email: "alicesmith@example.com",
		content: "Thank you for the project update. It looks great! I've gone through the report, and the progress is impressive. The team has done a fantastic job, and I appreciate the hard work everyone has put in.\n\nI have a few minor suggestions that I'll include in the attached document.\n\nLet's discuss these during our next meeting. Keep up the excellent work!\n\nBest regards, Alice",
		created_at: "2023-10-22T09:00:00",
        updated_at: "2023-10-22T09:00:00",
        remind_at: "2023-10-22T10:30:00",
	}
    ]


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
				</div>
                
				<Separator />
				
				<Tabs.Content value="all" class="m-0">
                    <!-- Notes List Start -->

                    <!-- if selected add bg-muted else Not in that button class -->
                    <!-- <button class="hover:bg-accent flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all bg-muted" on:click={() => mailStore.setMail(item.id)}> -->
                    <ScrollArea class="h-screen">
                        <div class="flex flex-col gap-2 p-4 pt-0">
                            {#each mails as item}
                                <button class="hover:bg-accent flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all" on:click={() => mailStore.setMail(item.id)}>
                                    <div class="flex w-full flex-col gap-1">
                                        <div class="flex items-center">
                                            <div class="flex items-center gap-2">
                                                <span class="flex h-2 w-2 rounded-full bg-blue-600" />
                                                <div class="font-semibold">{item.title}</div>
                                            </div>

                                            <!-- ml-auto text-xs text-muted-foreground -->
                                             <!-- Add this class if selcted or smething for time wala class -->
                                            <div class="ml-auto text-xs text-foreground">
                                                { item.updated_at }
                                            </div>
                                        </div>
                                    </div>
                                    <div class="text-muted-foreground line-clamp-2 text-xs">
                                        {item.content.substring(0, 300)}
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <Badge> Remind me:  {item.remind_at} </Badge>
                                    </div>
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
		<!-- <Resizable.Handle withHandle />
		<Resizable.Pane defaultSize={defaultLayout[2]}>
			<MailDisplay mail={mails.find((item) => item.id === $mailStore.selected) || null} />
		</Resizable.Pane> -->

	</Resizable.PaneGroup>
</div>