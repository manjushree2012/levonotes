<script>
    export let mails = [];
    export let selectedNoteId;
    export let selectMail;
</script>

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
                    <!-- <Badge>
                        <BellRing class="mr-2 h-4 w-4" />
                         Remind me:  {item.reminder.reminder_time_readable} 
                    </Badge> -->
                </div>
            {/if }
        </button>
    {/each}
</div>