<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button/index.js";

    import Code from "lucide-svelte/icons/code";
</script>
  
  <div class="flex min-h-screen w-full flex-col">
    <main class="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
        <section class="mx-auto flex max-w-[980px] flex-col items-center gap-2 py-8 md:py-12 md:pb-8 lg:py-24 lg:pb-20">
          <Dialog.Root>
            <Dialog.Trigger>
              <a href="#" class="inline-flex items-center rounded-lg bg-muted px-3 py-1 text-sm font-medium" previewlistener="true">
                <svg width="24" 
                height="24" 
                stroke="currentColor" 
                stroke-width="2" 
                class="lucide-icon lucide lucide-blocks size-4" 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke-linecap="round" 
                stroke-linejoin="round">
                    <rect width="7" height="7" x="14" y="3" rx="1"></rect>
                    <path d="M10 21V8a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1H3"></path>
                </svg>

                <div role="none" data-orientation="vertical" data-melt-separator="" data-separator-root="" class="shrink-0 bg-border w-[1px] mx-2 h-4"></div> 
                <span data-svelte-h="svelte-qkob9k">Before you get started</span>
                <svg width="24" height="24" stroke="currentColor" stroke-width="2" class="lucide-icon lucide lucide-arrow-right ml-1 size-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M5 12h14"></path>
                        <path d="m12 5 7 7-7 7"></path>
                </svg>
            </a>
            </Dialog.Trigger>
            <Dialog.Content>
              <Dialog.Header>
                <Dialog.Title>Do not enter sensitive information in your notes.</Dialog.Title>
                <Dialog.Description>
                  This is just a demo application created as a side project by me. Please, do not under any circumstances, enter any senitive information in your notes. The content is not encrypted.
                </Dialog.Description>
              </Dialog.Header>
            </Dialog.Content>
          </Dialog.Root>
            <h1 class="text-center text-3xl font-bold leading-tight tracking-tighter md:text-6xl lg:leading-[1.1] hidden md:block">
                Capture your ideas, Anytime, Anywhere
            </h1> 
            <h1 class="text-center text-3xl font-bold leading-tight tracking-tighter md:text-6xl lg:leading-[1.1] md:hidden">
                Examples
            </h1> 
            <p class="max-w-[750px] text-center text-lg text-muted-foreground sm:text-xl text-balance">
                Sync across devices, so your notes are always with you. Levonotes will and always be free.
            </p>
            <section class="flex w-full items-center justify-center space-x-4 py-4 md:pb-10">
                <Button href="/login">Login</Button>
                <Button href="/signup" variant="secondary">Sign Up</Button>
                <Button href="https://github.com/manjushree2012/codepulse" variant="ghost">
                  <Code class="mr-2 h-4 w-4" />
                  Github
                </Button>
            </section>
                       
          <figure class="max-w-lg">
            <img class="h-auto max-w-full" src="/images/demo.png" alt="image descriptio2n">
            <figcaption class="mt-2 text-sm text-center text-gray-500 dark:text-gray-400">
              Analyse all the code quality metrics you need for your project here
            </figcaption>
          </figure>

          <div class="mt-24">
            <h1 class="scroll-m-20 text-4xl font-bold tracking-tight">Works with programming language of your choice</h1>
            <div class="flex gap-8 md:gap-20 items-center justify-center mt-10 flex-wrap">
              <img class="object-contain h-32 w-48" src="/images/python-logo.png" alt="Python">
              <img class="object-contain h-32 w-48" src="/images/js-logo.png" alt="Javascript">
            </div>
          </div>
        </section>
    </main>
  </div>

  