<script>
    import { onDestroy } from 'svelte'; // Import onDestroy

    export let message = '';
    export let visible = false;

    // Automatically hide the toast after a few seconds
    let timer;
    $: if (visible) {
        timer = setTimeout(() => {
            visible = false;
        }, 3000); // Show for 3 seconds
    }

    // Clear the timer when the component is destroyed
    onDestroy(() => {
        clearTimeout(timer);
    });
</script>

<div class={`fixed bottom-5 right-5 transition-opacity duration-300 ${visible ? 'opacity-100' : 'opacity-0'}`}>
     <div class="bg-green-500 text-white p-4 rounded-lg shadow-lg">
        {message}
    </div>
</div>