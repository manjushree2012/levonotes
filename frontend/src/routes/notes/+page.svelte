<script>
    import { writable } from 'svelte/store';
    import { invalidateAll } from '$app/navigation';

    import NoteDisplay from './(components)/note-display.svelte';
    import NoteList from './(components)/note-list.svelte';

    import { Search } from 'lucide-svelte';
    import { X } from 'lucide-svelte';
    import { Input } from "$lib/components/ui/input";
    import Toast from "$lib/components/ui/Toast.svelte"
    import * as Resizable from "$lib/components/ui/resizable";
    import { Separator } from "$lib/components/ui/separator";
    import * as Tabs from "$lib/components/ui/tabs";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import { Button } from "$lib/components/ui/button";
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

    $: selectedNote = $mails.find(mail => mail.id === $selectedNoteId);

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
                        <NoteList {mails} {selectedNoteId} {selectMail} />
                    </ScrollArea>
				</Tabs.Content>
			</Tabs.Root>
		</Resizable.Pane>

        <!--Display note component seperate from here -->
		<Resizable.Handle withHandle />
		<Resizable.Pane defaultSize={defaultLayout[2]}>
                <NoteDisplay 
                    note={selectedNote}
                    reminderDateTime={reminderDateTime}
                    remind_mail={$remind_mail}
                    isLoading={isLoading}
                    deleteNote={deleteNote}
                    handleContentUpdate={handleContentUpdate}
                />
		</Resizable.Pane>
	</Resizable.PaneGroup>
</div>