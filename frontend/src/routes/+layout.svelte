<!-- <script>
	import '../app.css';
</script>

<slot></slot>

 -->





 <script>
	import '../app.css';
</script>

<header class="sticky top-0 flex h-16 items-center gap-4 border-b bg-background px-4 md:px-6">
	<nav
	  class="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6">
	  <a href="/" class="flex items-center gap-2 text-lg font-semibold md:text-base">
		  <img src="/images/header.png" alt="codePulse">
	  </a>
	  <a href="/" class="text-foreground transition-colors hover:text-foreground">
		Home
	  </a>
	  <a href="##" class="text-muted-foreground transition-colors hover:text-foreground">
		Services
	  </a>
	  <a href="##" class="text-muted-foreground transition-colors hover:text-foreground">
		Limitations
	  </a>
	  <a href="##" class="text-muted-foreground transition-colors hover:text-foreground">
		About
	  </a>
	  <a href="https://github.com/manjushree2012/codepulse" class="text-muted-foreground transition-colors hover:text-foreground">
		  Github
		</a>
	</nav>
	<div class="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
	</div>
</header>

<slot></slot>

<footer class="bg-white rounded-lg shadow m-4 dark:bg-gray-800">
    <div class="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between">
      <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">© 2024 CodePulse. All Rights Reserved.
    </span>
    <ul class="flex flex-wrap items-center mt-3 text-sm font-medium text-gray-500 dark:text-gray-400 sm:mt-0">
        <li>
            <a href="https://www.linkedin.com/in/manjushree2012/" class="hover:underline me-4 md:me-6">About me</a>
        </li>
        <li>
            <a href="#" class="hover:underline me-4 md:me-6">Releases</a>
        </li>
        <li>
            <a href="#" class="hover:underline me-4 md:me-6">Report a bug</a>
        </li>
    </ul>
    </div>
</footer>

<style></style>
