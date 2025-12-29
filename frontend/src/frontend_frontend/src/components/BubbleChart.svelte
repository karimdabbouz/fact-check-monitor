<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    export let topicCounts = [];

    let svgElement;
    let width = 800;
    let height = 600;

    const drawChart = () => {
        if (!svgElement || topicCounts.length === 0) {
            d3.select(svgElement).remove();
            return;
        }

        const container = svgElement.parentElement;
        width = container.clientWidth;
        height = Math.max(container.clientHeight, 500);

        d3.select(svgElement).selectAll('*').remove();

        const margin = { top: 20, right: 20, bottom: 20, left: 20 };
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;

        const svg = d3.select(svgElement)
            .attr('width', width)
            .attr('height', height);

        const chartGroup = svg.append('g')
            .attr('class', 'bubble-wrapper')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);

        const data = topicCounts.map(d => ({
            topic: d.topic,
            count: d.count,
            id: d.topic,
            x: Math.random() * innerWidth,
            y: Math.random() * innerHeight
        }));

        const maxCount = d3.max(data, d => d.count);
        const minCount = d3.min(data, d => d.count);
        const radiusScale = d3.scaleSqrt()
            .domain([minCount, maxCount])
            .range([innerWidth / 10 / 2.5, innerWidth / 3 / 2.5]);

        const simulation = d3.forceSimulation(data)
            .force('forceX', d3.forceX(innerWidth / 2))
            .force('forceY', d3.forceY(innerHeight / 2))
            .force('charge', d3.forceManyBody().strength(-50))
            .force('collision', d3.forceCollide(d => radiusScale(d.count) + 2));

        // Drag Functions
        const dragstarted = (event, d) => {
            if (!event.active) simulation.alphaTarget(.03).restart();
                d.fx = d.x;
                d.fy = d.y;
        }

        const dragged = (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
        }

        const dragended = (event, d) => {
            if (!event.active) simulation.alphaTarget(.03);
                d.fx = null;
                d.fy = null; // one of these makes the simulation stop and keep the nodes in the specific place
        }

        const node = chartGroup.selectAll('g.bubble')
            .data(data, d => d.id)
            .join('g')
            .attr('class', 'bubble')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended)
            );

        node.append('circle')
            .attr('r', d => radiusScale(d.count))
            .style('fill', (d, i) => d3.schemeCategory10[i % 10])
            .style('opacity', 0.7);

        simulation.on('tick', () => {
            node.attr('transform', d => `translate(${d.x}, ${d.y})`);
        });
    };

    onMount(() => {
        drawChart();
    });

    $: if (topicCounts && topicCounts.lenght > 0) {
        drawChart();
    };
</script>

<div class="bubble-chart-container w-full h-96 md:h-screen">
    <svg bind:this={svgElement} class="w-full h-full"></svg>
</div>

<style>
    :global(.bubble-chart-container) {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 8px;
    }
</style>

