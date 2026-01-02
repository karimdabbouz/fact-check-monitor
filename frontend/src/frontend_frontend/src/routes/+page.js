export const load = async ({ fetch, url}) => {
    const getDateString = (date) => date.toISOString().split('T')[0];
    
    const published_before = url.searchParams.get('published_before') || getDateString(new Date());
    const published_after = url.searchParams.get('published_after') || getDateString(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000));
    const medium = url.searchParams.get('medium') || '';
    
    const params = new URLSearchParams({
        published_after,
        published_before,
        ...(medium && { medium })
    });
    
    const res = await fetch(`http://localhost:8000/topic-counts?${params}`);
    const topicCounts = await res.json();
    
    return {
        topicCounts,
        published_after,
        published_before,
        medium
    };
};