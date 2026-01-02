<script>
    import { goto } from '$app/navigation';
    import "../../../main.css";
    import ClaimBubbleChart from '../../../components/ClaimBubbleChart.svelte';

    export let data;

    let topic = data.topic;
    let published_after = data.published_after;
    let published_before = data.published_before;
    let medium = data.medium;
    let articles = data.articles;

    $: articles = data.articles.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));

    const handleFilterChange = () => {
        const newSearchParams = new URLSearchParams();
        newSearchParams.append('published_after', published_after);
        newSearchParams.append('published_before', published_before);
        if (medium) {
            newSearchParams.append('medium', medium);
        };
        goto(`/topic/${topic}?${newSearchParams.toString()}`);
    };

</script>


<nav class="grid grid-rows-2 gap-y-4 h-20 p-4 w-full sticky top-0 shadow-md" style="background-color: white;">
    <div class="row-span-1 flex flex-row justify-between">
        <div class="self-center">
            <h1 class="text-4xl font-bold">Thema: <span style="color: #FF2F2F; font-weight: 400;">{topic}</span></h1>
        </div>
        <div class="justify-self-end self-center">
            <div class="flex flex-col md:flex-row gap-4 items-end">
                <div class="flex-1">
                    <input
                        type="date"
                        id="published_after"
                        bind:value={published_after}
                        on:change={handleFilterChange}
                        class="date-selector px-2"
                    />
                </div>
                <div class="flex-1">
                    <input
                        type="date"
                        id="published_before"
                        bind:value={published_before}
                        on:change={handleFilterChange}
                        class="date-selector px-2"
                    />
                </div>
                <div class="flex-1">
                    <select
                        id="medium"
                        bind:value={medium}
                        on:change={handleFilterChange}
                        class="medium-selector px-2"
                    >
                        <option value="">Alle Medien</option>
                        <option value="correctiv">Correctiv</option>
                        <option value="br-faktenfuchs">BR Faktenfuchs</option>
                        <option value="tagesschau-faktenfinder">Tagesschau Faktenfinder</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
    <div class="row-span-1 flex flex-row justify-between">
        <div class="flex flex-row gap-x-4 justify-between">
            <div>{published_after} bis {published_before}</div>
            <div>|</div>
            <div>{medium ? medium : 'Alle Medien'}</div>
            <div>|</div>
            <div>{articles.length} Faktenchecks</div>
        </div>
    </div>
</nav>

<!-- <main class="grid grid-cols-1 min-h-screen" style="background-color: #F4EDE8;">
    <ClaimBubbleChart />
</main> -->

<main class="grid grid-cols-1 min-h-screen" style="background-color: #F4EDE8;">
    <section class="max-w-4xl mx-auto w-full px-4 mt-12">
        
        <div class="space-y-6">
            {#each articles as article (article.id)}
                <a href={article.url} target="_blank" rel="noopener noreferrer" class="block">
                    <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-200">
                        <div class="bg-red-50 border-l-4 border-red-500 p-4">
                            <p class="text-sm font-semibold text-red-700">BEHAUPTUNG</p>
                            <p class="text-lg font-bold text-gray-900 mt-1">"{article.claim || 'Behauptung nicht verfügbar'}"</p>
                        </div>
                        <div class="p-6">
                            <h3 class="text-xl font-semibold mb-3 hover:text-red-600 transition-colors">{article.headline || 'Kein Titel verfügbar'}</h3>
                            <p class="text-gray-700 mb-4">{article.teaser || 'Keine Beschreibung verfügbar'}</p>
                            <div class="flex justify-between items-center text-sm text-gray-500 pt-4 border-t">
                                <span>{article.medium}</span>
                                <span>{article.published_at ? new Date(article.published_at).toLocaleDateString('de-DE') : 'Kein Datum'}</span>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    </section>
</main>

<a 
    href="/" 
    class="fixed bottom-4 left-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
>
    ← Zurück zur Themenübersicht
</a>