<script>
	import { onMount, onDestroy } from 'svelte';
	import { Editor } from '@tiptap/core';
	import StarterKit from '@tiptap/starter-kit';

	let element;
	let editor;

	export let content;

	 // Watch for changes in the content prop
	 $: if (editor && content !== editor.getHTML()) {
        editor.commands.setContent(content); // Update editor content when prop changes
    }

	onMount(() => {
		editor = new Editor({
			element: element,
			extensions: [StarterKit],
			content: content,
			onTransaction: () => {
				// force re-render so `editor.isActive` works as expected
				editor = editor;
			},
			onUpdate({editor}) {
				const content = editor.getHTML()
				
				updateContent(content)

				
			}
		});
	});

	onDestroy(() => {
		if (editor) {
			editor.destroy();
		}
	});

	async function updateContent(content) {
		const title = "Shopping List"
		try {
            const response = await fetch('http://127.0.0.1:5000/note', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, content })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Update successful:', data);
        } catch (error) {
            console.error('Error updating content:', error);
        }
	}
</script>

{#if editor}
	<button
		on:click={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
		class:active={editor.isActive('heading', { level: 1 })}
	>
		H1
	</button>
	<button
		on:click={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
		class:active={editor.isActive('heading', { level: 2 })}
	>
		H2
	</button>
	<button
		on:click={() => editor.chain().focus().setParagraph().run()}
		class:active={editor.isActive('paragraph')}
	>
		P
	</button>
{/if}

<div bind:this={element} />

<style>
	button.active {
		background: black;
		color: white;
	}
</style>
