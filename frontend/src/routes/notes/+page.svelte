<script>
    import { onMount } from 'svelte';
    import Tiptap from '$lib/Tiptap.svelte'

    import { Search } from 'lucide-svelte';


    import { writable } from 'svelte/store';
    import { DateInput } from 'date-picker-svelte'

    import { Input } from "$lib/components/ui/input";
    import { BellRing } from 'lucide-svelte';

    import Reload from "svelte-radix/Reload.svelte";




    let reminderDateTime = new Date()
    let mails = [];
    let loading = true;
    let error = null;

    let saveTimeout;
    let saveInterval = 5000; // Set to 5000 ms (5 seconds) or 10000 ms (10 seconds)
    let currentContent = '';

    let isLoading = false; // Add this line

    const selectedNoteId = writable(null)

    let searchQuery = writable('');

     // Reactive statement to call the search API when the search query changes
     $: searchQueryValue = $searchQuery;
        $: {
            if (searchQueryValue) {
                searchAPI(searchQueryValue);
            }
        }

        // Function to call the search API
    async function searchAPI(query) {
        console.log('Search changed')
        console.log(query)

        
        try {
            const response = await fetch(` http://127.0.0.1:5000/notes/search?query=${query}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // const results = await response.json();
            mails = await response.json()
            // console.log('Search results:', results);
            // Update your notes or display results as needed
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    }

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

    async function handleContentUpdate(event) {
        currentContent = event.detail.content

        // Clear the existing timeout if it exists
        if (saveTimeout) {
            clearTimeout(saveTimeout);
        }

         // Set a new timeout to save content after the defined interval
         saveTimeout = setTimeout(() => {
            saveContent();
        }, saveInterval);
    }

    async function saveContent() {
        const title = "Shopping List"

        isLoading = true; // Set loading to true before saving

		try {
            const response = await fetch(`http://127.0.0.1:5000/note/${selectedNote.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, content: currentContent })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Update successful:', data);
        } catch (error) {
            console.error('Error updating content:', error);
        } finally {
            isLoading = false; // Set loading to false after saving
        }
    }

    async function deleteNote(selectedNote) {
        console.log(selectedNote)

        if ($selectedNoteId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/note/${$selectedNoteId}`, {
                    method: 'DELETE',
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                console.log('Delete successful:', data);

                // Optionally, you can remove the deleted note from the mails array
                mails = mails.filter(mail => mail.id !== $selectedNoteId);
                selectedNoteId.set(null); // Clear the selected note
            } catch (error) {
                console.error('Error deleting note:', error);
            }
        }
    }

    // Reactive variable to get the selected note object
    $: selectedNote = mails.find(mail => mail.id === $selectedNoteId);

    // Reactive statement to call the API when the date changes
    $: {
        updateDateAPI(reminderDateTime);
    }

    async function updateDateAPI(newDate) {
        if (selectedNote) {
            console.log('Reminder changed')

            const email = "levo@mailinator.com"
            const message = "Random email body."
            const reminder_time = newDate
            const note_id = selectedNote.id

            try {
                const response = await fetch(`http://127.0.0.1:5000/reminder/${note_id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, message, reminder_time }),
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
                        <NotebookPen class="mr-2 h-4 w-4" />
                        Create New
                      </Button>
				</div>
                
				<Separator />

                <div
					class="bg-background/95 supports-[backdrop-filter]:bg-background/60 p-4 backdrop-blur"
				>
					<form>
						<div class="relative">
							<Search
								class="text-muted-foreground absolute left-2 top-[50%] h-4 w-4 translate-y-[-50%]"
							/>
							<Input 
                                placeholder="Search" 
                                class="pl-8"
                                bind:value={$searchQuery} 
                                on:input={() => searchQuery.set($searchQuery)}
                            />
						</div>
					</form>
				</div>
				
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
                                            <Badge>
                                                <BellRing class="mr-2 h-4 w-4" />
                                                 Remind me:  {item.reminder.reminder_time_readable} </Badge>
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
                                <Button 
                                    class="ml-auto"  
                                    on:click={deleteNote}>
                                        <Trash2 class="mr-2 h-4 w-4"/>
                                        Delete
                                </Button>
                            <DateInput 
                                bind:value={reminderDateTime}
                                timePrecision="minute"                            
                            />
                            <Separator orientation="vertical" class="mx-1 h-6" />
                        </div>
                        <div class="ml-auto flex items-center gap-2">
                            {#if isLoading}
                                <Reload class="mr-2 h-4 w-4 animate-spin" />
                                Saving ...
                            {/if}

                        </div>
                        <Separator orientation="vertical" class="mx-2 h-6" />
                    </div>
                {/if}
                <Separator />
                {#if selectedNote}
                    <div class="flex h-full flex-1 flex-col overflow-hidden">
                        <div class="flex items-start p-4">
                            <div class="text-muted-foreground ml-auto text-xs">
                                Updated: { selectedNote.updated_at_readable }
                            </div>
                        </div>

                        <div class="flex-1 overflow-y-auto whitespace-pre-wrap p-4 text-sm">
                            <Tiptap content={selectedNote.content} on:contentUpdated={handleContentUpdate} />
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