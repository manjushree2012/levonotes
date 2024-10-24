<script>
    import { writable } from 'svelte/store';
    import { invalidateAll } from '$app/navigation';

    import Tiptap from '$lib/Tiptap.svelte'
    import { BellRing } from 'lucide-svelte';
    import Reload from "svelte-radix/Reload.svelte";
    import { BellPlus } from 'lucide-svelte';
    import { Search } from 'lucide-svelte';
    import { X } from 'lucide-svelte';
    import { Input } from "$lib/components/ui/input";
    import Toast from "$lib/components/ui/Toast.svelte"
    import { DateInput } from 'date-picker-svelte'
    import * as Resizable from "$lib/components/ui/resizable";
    import { Separator } from "$lib/components/ui/separator";
    import * as Tabs from "$lib/components/ui/tabs";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import { Badge } from "$lib/components/ui/badge";
    import { Button } from "$lib/components/ui/button";
    import { Trash2 } from 'lucide-svelte';
    import { NotebookPen } from 'lucide-svelte';

    export let data;
    let mails = writable(data.notes)
    $: mails.set(data.notes); 

    let toastVisible = false;
    let toastMessage = '';

     // Function to show the toast
     function showToast(message) {
        toastMessage = message;
        toastVisible = true;
    }

    let reminderDateTime = new Date();
    let minDateTime = new Date();

    // Reactive statement to update reminderDateTime based on selectedNote
    // $: {
    //     if (selectedNote && selectedNote.reminder && selectedNote.reminder.reminder_time) {
    //         console.log('Yo note ko reminder cha')
    //         reminderDateTime = new Date(selectedNote.reminder.reminder_time);
    //     } else {
    //         reminderDateTime = new Date();
    //     }
    // }

    // let mails = writable([])
    let loading = true;
    let error = null;

    let saveTimeout;
    let saveInterval = 5000; // Set to 5000 ms (5 seconds) or 10000 ms (10 seconds)
    let currentContent = '';

    let isLoading = false; // Add this line

    const selectedNoteId = writable(null)

    let searchQuery = writable('');
    let remind_mail = writable('')
    let debounceTimeout;

     // Reactive statement to update remind_mail based on selectedNote
     $: {
        if (selectedNote && selectedNote.reminder && selectedNote.reminder.email) {
            remind_mail.set(selectedNote.reminder.email);
        } else {
            remind_mail.set(''); // or set to null if you prefer
        }
    }

     // Reactive statement to call the search API when the search query changes
     $: searchQueryValue = $searchQuery;

     $: {
        if (debounceTimeout) {
            clearTimeout(debounceTimeout);
        }
        if (searchQueryValue) {
            debounceTimeout = setTimeout(() => {
                searchAPI(searchQueryValue);
            }, 1000); // 1 second of debounce time
        }
    }

      // Function to format the date in local format and calculate time difference
      function formatDate(updatedOn) {
        const updatedDate = new Date(updatedOn);
        const now = new Date();
        const timeDiff = now - updatedDate; // Time difference in milliseconds

        // Format the date to local string
        const localDateString = updatedDate.toLocaleString();

        // Calculate time difference in a readable format
        const seconds = Math.floor(timeDiff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        let timeDifference;

        if (days > 0) {
            timeDifference = `${days} day${days > 1 ? 's' : ''} ago`;
        } else if (hours > 0) {
            timeDifference = `${hours} hour${hours > 1 ? 's' : ''} ago`;
        } else if (minutes > 0) {
            timeDifference = `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        } else {
            timeDifference = `${seconds} second${seconds > 1 ? 's' : ''} ago`;
        }

        // return { localDateString, timeDifference };
        return timeDifference
    }

    function formatReminderDate(reminderTime) {
    const reminderDate = new Date(reminderTime);
    const now = new Date();
    const timeDiff = reminderDate - now; // Time difference in milliseconds

    // Format the date to local string
    const localDateString = reminderDate.toLocaleString();

    // Calculate time difference in a readable format
    const seconds = Math.floor(timeDiff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    let timeDifference;

    if (days > 0) {
        timeDifference = `${days} day${days > 1 ? 's' : ''} from now`;
    } else if (hours > 0) {
        timeDifference = `${hours} hour${hours > 1 ? 's' : ''} from now`;
    } else if (minutes > 0) {
        timeDifference = `${minutes} minute${minutes > 1 ? 's' : ''} from now`;
    } else {
        timeDifference = `${seconds} second${seconds > 1 ? 's' : ''} from now`;
    }

    return timeDifference;
}

    // Function to call the search API
    async function searchAPI(query) {      
        try {
            const response = await fetch(` http://127.0.0.1:5000/api/notes/search?query=${query}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // const results = await response.json();
            const notes = await response.json()
            mails.set(notes)
            // console.log('Search results:', results);
            // Update your notes or display results as needed
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    }

    export let defaultLayout = [265, 440, 655];
	export let defaultCollapsed = false;

	let isCollapsed = defaultCollapsed;

	function onLayoutChange(sizes) {
		document.cookie = `PaneForge:layout=${JSON.stringify(sizes)}`;
	}

    function selectMail(id) {
        selectedNoteId.set(id);
    }

    async function handleContentUpdate(event) {
        currentContent = event.detail.content;
        isLoading = true;

        if (saveTimeout) {
            clearTimeout(saveTimeout);
        }

        saveTimeout = setTimeout(async () => {
            const formData = new FormData();
            formData.append('id', $selectedNoteId);
            formData.append('content', currentContent);
            formData.append('title', 'Shopping List');

            try {
                const response = await fetch('?/update', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) throw new Error('Failed to save');
                
                await invalidateAll(); // Refresh the page data
            } catch (error) {
                console.error('Error saving:', error);
            } finally {
                isLoading = false;
            }
        }, saveInterval);
    }

    async function deleteNote(selectedNote) {
        if ($selectedNoteId) {
            const formData = new FormData();
            formData.append('id', $selectedNoteId);

            try {
                const response = await fetch('?/delete', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) throw new Error('Delete failed');
                
                showToast('Note deleted successfully!');

                selectedNoteId.set(null);
                await invalidateAll();
            } catch (error) {
                console.error('Error deleting:', error);
            }
        }
    }

    // Reactive variable to get the selected note object
    $: selectedNote = $mails.find(mail => mail.id === $selectedNoteId);

    async function updateDateAPI() {
        if (selectedNote) {
            const formData = new FormData();
            formData.append('noteId', selectedNote.id);
            formData.append('email', $remind_mail);
            formData.append('reminderTime', reminderDateTime.toISOString());
            formData.append('message', 'Random email body.');

            try {
                const response = await fetch('?/updateReminder', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) throw new Error('Failed to update reminder');
                
                showToast('Reminder set successfully!');
                await invalidateAll();
            } catch (error) {
                console.error('Error updating reminder:', error);
            }
        }
    }
</script>

<Toast message={toastMessage} visible={toastVisible} />

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

                            {#if $searchQuery} <!-- Show the cross only if there's a search query -->
                                <button class="absolute right-2 top-[50%] translate-y-[-50%]" 
                                on:click={
                                            () => { 
                                                searchQuery.set('');
                                                getNotes();
                                        }}>
                                    <X class="h-4 w-4 text-muted-foreground" />
                                </button>
                            {/if}

						</div>
					</form>
				</div>
				
				<Tabs.Content value="all" class="m-0">
                    <!-- Notes List Start -->

                    <ScrollArea class="h-screen">
                        <div class="flex flex-col gap-2 p-4 pt-0">
                            {#each $mails as item}
                                <button 
                                class={`hover:bg-accent flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all ${$selectedNoteId === item.id ? 'bg-muted' : ''}`} 
                                on:click={() => selectMail(item.id) }>
                                    <div class="flex w-full flex-col gap-1">
                                        <div class="flex items-center">
                                            <div class="flex items-center gap-2">
                                            </div>

                                            <div class="ml-auto text-xs text-foreground">
                                                { formatDate(item.updated_on) }
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
                                                 Remind me:  
                                                 { formatReminderDate(item.reminder.reminder_time) }
                                                </Badge>
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
                            Mail to:
                            <Input
                                type="email"
                                placeholder="Email address"
                                class="pl-8"
                                bind:value={$remind_mail} 
                            />
                            @
                            <DateInput 
                                bind:value={reminderDateTime}
                                timePrecision="minute"      
                                min={minDateTime}  
                                placeholder="Pick a future datetime"                    
                            />                            
                            <Button variant="outline"  on:click={() => updateDateAPI() }>
                                <BellPlus class="mr-2 h-4 w-4" />
                              </Button>
                            <Separator orientation="vertical" class="mx-1 h-6" />
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
                        <Separator orientation="vertical" class="mx-2 h-6" />
                    </div>
                {/if}
                <Separator />
                {#if selectedNote}
                    <div class="flex h-full flex-1 flex-col overflow-hidden">
                        <div class="flex items-start p-4">
                            <div class="text-muted-foreground ml-auto text-xs">
                                Updated: 
                                { formatDate(selectedNote.updated_on) }
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