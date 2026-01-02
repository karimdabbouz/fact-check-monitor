<script>
    import * as d3 from 'd3';

    let svgElement;
    let width;
    let height;

    const colors = ['#FF7A6B', '#E6C6A8', '#9FC3A1', '#FBA47E', '#C3C77A', '#B3A1C8', '#FF9A9A', '#E8C96A', '#8FA8C8', '#7FB7B2', '#F6B58E'];

    const dummyClaims = [
        'Die Impfung wurde zu schnell entwickelt und ist daher nicht sicher.',
        'Elektroautos sind umweltschädlicher als Benzinfahrzeuge.',
        'Migration verursacht wirtschaftliche Instabilität.',
        'Der Klimawandel ist nicht menschengemacht.',
        'Globale Eliten kontrollieren die Regierungen der Welt.',
        'Armutsbekämpfung ist der wichtigste Zweck von Sozialprogrammen.',
        'Künstliche Intelligenz wird alle Arbeitsplätze ersetzen.',
        'Die Medien berichten nicht wahrheitsgetreu über Krisen.',
        'Erneuerbare Energien können fossil fuels vollständig ersetzen.',
        'Wirtschaftsungleichheit schadet dem sozialen Zusammenhalt.',
        'Technologie-Großkonzerne haben zu viel Macht in der Gesellschaft.'
    ];

    const drawChart = () => {
        if (!svgElement) return;

        const container = svgElement.parentElement;
        width = container.clientWidth;
        height = 1000;

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

        const data = dummyClaims.map((claim, i) => ({
            claim: claim,
            id: i,
            x: Math.random() * innerWidth,
            y: Math.random() * innerHeight
        }));

        const bubbleRadius = 120;

        const simulation = d3.forceSimulation(data)
            .force('forceX', d3.forceX(innerWidth / 2))
            .force('forceY', d3.forceY(innerHeight / 2))
            .force('charge', d3.forceManyBody().strength(-50))
            .force('collision', d3.forceCollide(bubbleRadius + 2));

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
                d.fy = null;
        }

        const node = chartGroup.selectAll('g.bubble')
            .data(data, d => d.id)
            .join('g')
            .attr('class', 'bubble')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended)
            )
            .on('mouseenter', function() {
                d3.select(this).raise();
                d3.select(this).select('circle')
                    .style('opacity', 1);
                d3.select(this).select('text')
                    .style('font-weight', 'bold');
            })
            .on('mouseleave', function() {
                d3.select(this).select('circle')
                    .style('opacity', 0.7);
                d3.select(this).select('text')
                    .style('font-weight', 'normal');
            });

        node.append('circle')
            .attr('r', bubbleRadius)
            .style('fill', (d, i) => colors[i % colors.length])
            .style('opacity', 0.7);

        node.append('text')
            .text(d => d.claim)
            .style('font-size', '20px')
            .attr('fill', '#310000')
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .style('pointer-events', 'none')
            .attr('dy', '0.3em')
            .attr('x', 0)
            .attr('y', 0);

        simulation.on('tick', () => {
            node.attr('transform', d => `translate(${d.x}, ${d.y})`);
        });
    };

    $: if (svgElement) {
        drawChart();
    };
</script>

<div class="w-full overflow-hidden">
    <svg bind:this={svgElement}></svg>
</div>

