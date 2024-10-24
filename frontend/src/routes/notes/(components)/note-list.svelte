<script>
    import { Badge } from "$lib/components/ui/badge";
    import { BellRing } from 'lucide-svelte';

    export let mails = [];
    export let selectedNoteId;
    export let selectMail;

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
</script>

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