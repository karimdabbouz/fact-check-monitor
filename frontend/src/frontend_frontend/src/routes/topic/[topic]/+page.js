export const load = async ({ fetch, url, params }) => {
    const topic = params.topic;
    const published_after = url.searchParams.get('published_after') || '';
    const published_before = url.searchParams.get('published_before') || '';
    const medium = url.searchParams.get('medium') || '';

    const apiParams = new URLSearchParams();
    apiParams.append('topic', topic);
    if (published_after) apiParams.append('published_after', published_after);
    if (published_before) apiParams.append('published_before', published_before);
    if (medium) apiParams.append('medium', medium);

    const res = await fetch(`http://localhost:8000/articles-by-topic?${apiParams}`);
    const articles = await res.json();

    return {
        topic,
        published_after,
        published_before,
        medium,
        articles
    };
};