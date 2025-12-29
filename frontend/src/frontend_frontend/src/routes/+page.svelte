<script>
    import "../main.css";
    import BubbleChart from '../components/BubbleChart.svelte';
    
    export let data;
    
    let published_after = data.published_after;
    let published_before = data.published_before;
    let medium = data.medium;
    let topicCounts = data.topicCounts;
    
    const handleFilterChange = () => {
        const params = new URLSearchParams({
            published_after,
            published_before,
            ...(medium && { medium })
        });
        window.location.search = params.toString();
    };
</script>

<main class="grid grid-cols-1 md:grid-cols-6 grid-rows-[auto_auto_1fr] min-h-screen gap-y-6 md:gap-y-10 px-4 md:px-10 py-6 md:py-10 bg-gray-50">

    <!-- First Row: Hero Section (Headline + Subline) -->
    <section class="col-span-full text-center">
        <h1 class="text-6xl sm:text-7xl md:text-8xl font-extrabold text-gray-900 leading-tight">
            Fact-Checking <span class="text-blue-600">Observatory</span>
        </h1>
        <p class="mt-4 text-xl sm:text-2xl text-gray-600 max-w-3xl mx-auto">
            What topics dominate fact-checking right now?
            Observe agenda-setting, framing, and imbalance.
        </p>
    </section>

    <!-- Filter Bar -->
    <section class="col-span-full bg-white rounded-lg shadow p-6">
        <div class="flex flex-col md:flex-row gap-4 items-end">
            <div class="flex-1">
                <label for="published_after" class="block text-sm font-medium text-gray-700 mb-2">From</label>
                <input
                    type="date"
                    id="published_after"
                    bind:value={published_after}
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
            </div>
            <div class="flex-1">
                <label for="published_before" class="block text-sm font-medium text-gray-700 mb-2">To</label>
                <input
                    type="date"
                    id="published_before"
                    bind:value={published_before}
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
            </div>
            <div class="flex-1">
                <label for="medium" class="block text-sm font-medium text-gray-700 mb-2">Medium</label>
                <select
                    id="medium"
                    bind:value={medium}
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                    <option value="">All</option>
                    <option value="correctiv">Correctiv</option>
                    <option value="br-faktenfuchs">BR Faktenfuchs</option>
                    <option value="tagesschau-faktenfinder">Tagesschau Faktenfinder</option>
                </select>
            </div>
            <button
                on:click={handleFilterChange}
                class="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition"
            >
                Filter
            </button>
        </div>
    </section>

    <!-- Second Row: SVG Circles Section -->
    <section class="col-span-full py-8">
        <BubbleChart {topicCounts} />
    </section>
</main>
