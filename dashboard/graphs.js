/**
 * Vanilla Canvas-Based Graph Rendering System
 * graphs.js - Pure JavaScript graph rendering without external chart libraries
 * Provides fallback for Chart.js and pure DOM-based alternatives
 */

window.GraphRenderer = {
  /**
   * Create a line chart using Canvas API
   */
  createLineChart: function(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    const ctx = canvas.getContext('2d');
    const width = canvas.width || 800;
    const height = canvas.height || 300;
    
    const padding = 40;
    const chartWidth = width - (padding * 2);
    const chartHeight = height - (padding * 2);

    // Clear canvas
    ctx.fillStyle = options.backgroundColor || '#f5f0e8';
    ctx.fillRect(0, 0, width, height);

    // Draw axes
    ctx.strokeStyle = options.gridColor || '#d4cec2';
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();

    // Draw grid lines
    ctx.strokeStyle = options.gridColor || '#d4cec2';
    ctx.globalAlpha = 0.3;
    const gridLines = 5;
    for (let i = 0; i <= gridLines; i++) {
      const y = padding + (chartHeight / gridLines) * i;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(width - padding, y);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;

    // Draw line
    if (data && data.length > 0) {
      const maxValue = Math.max(...data, 1);
      ctx.strokeStyle = options.lineColor || '#c8401a';
      ctx.lineWidth = 2;
      ctx.beginPath();

      data.forEach((value, idx) => {
        const x = padding + (chartWidth / (data.length - 1)) * idx;
        const y = height - padding - ((value / maxValue) * chartHeight);
        
        if (idx === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });

      ctx.stroke();

      // Draw points
      ctx.fillStyle = options.pointColor || '#c8401a';
      data.forEach((value, idx) => {
        const x = padding + (chartWidth / (data.length - 1)) * idx;
        const y = height - padding - ((value / maxValue) * chartHeight);
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();
      });
    }

    return canvas;
  },

  /**
   * Create a bar chart using Canvas
   */
  createBarChart: function(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    const ctx = canvas.getContext('2d');
    const width = canvas.width || 800;
    const height = canvas.height || 300;

    const padding = 40;
    const chartWidth = width - (padding * 2);
    const chartHeight = height - (padding * 2);

    // Clear canvas
    ctx.fillStyle = options.backgroundColor || '#f5f0e8';
    ctx.fillRect(0, 0, width, height);

    // Draw axes
    ctx.strokeStyle = options.gridColor || '#d4cec2';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();

    // Draw bars
    if (data && data.length > 0) {
      const maxValue = Math.max(...data, 1);
      const barWidth = chartWidth / data.length;

      data.forEach((value, idx) => {
        const x = padding + (barWidth * idx) + (barWidth * 0.1);
        const barHeight = (value / maxValue) * chartHeight;
        const y = height - padding - barHeight;

        // Draw bar
        ctx.fillStyle = options.barColor || '#c8401a';
        ctx.fillRect(x, y, barWidth * 0.8, barHeight);

        // Draw label
        if (labels && labels[idx]) {
          ctx.fillStyle = options.textColor || '#0a0e14';
          ctx.font = '12px DM Mono';
          ctx.textAlign = 'center';
          ctx.fillText(labels[idx], x + (barWidth * 0.4), height - padding + 20);
        }
      });
    }

    return canvas;
  },

  /**
   * Create a pie chart using Canvas
   */
  createPieChart: function(canvasId, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    const ctx = canvas.getContext('2d');
    const width = canvas.width || 400;
    const height = canvas.height || 300;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 2 - 20;

    // Clear canvas
    ctx.fillStyle = options.backgroundColor || '#f5f0e8';
    ctx.fillRect(0, 0, width, height);

    // Calculate total
    const total = data.reduce((a, b) => a + b, 1);

    // Draw slices
    const colors = options.colors || [
      '#c8401a', '#1a4fd6', '#16a34a', '#f59e0b', '#8b5cf6'
    ];

    let currentAngle = -Math.PI / 2;

    data.forEach((value, idx) => {
      const sliceAngle = (value / total) * Math.PI * 2;

      // Draw slice
      ctx.fillStyle = colors[idx % colors.length];
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
      ctx.closePath();
      ctx.fill();

      // Draw label
      const labelAngle = currentAngle + sliceAngle / 2;
      const labelX = centerX + Math.cos(labelAngle) * (radius * 0.7);
      const labelY = centerY + Math.sin(labelAngle) * (radius * 0.7);

      if (labels && labels[idx]) {
        const percentage = Math.round((value / total) * 100);
        ctx.fillStyle = options.textColor || '#0a0e14';
        ctx.font = '12px DM Mono';
        ctx.textAlign = 'center';
        ctx.fillText(`${percentage}%`, labelX, labelY);
      }

      currentAngle += sliceAngle;
    });

    return canvas;
  },

  /**
   * Create a heatmap using DOM (table-based)
   */
  createHeatmapTable: function(containerId, data, options = {}) {
    const container = document.getElementById(containerId);
    if (!container) return null;

    const maxValue = Math.max(...data.flat(), 1);
    let html = '<div class="heatmap-container" style="display: grid; gap: 2px;">';

    data.forEach((row, rowIdx) => {
      row.forEach((value, colIdx) => {
        const intensity = value / maxValue;
        const hue = options.hue || 0; // Red
        const color = `hsl(${hue}, 100%, ${100 - (intensity * 50)}%)`;
        
        html += `<div class="heatmap-cell" style="
          width: 20px; height: 20px;
          background-color: ${color};
          border: 1px solid #ddd;
          border-radius: 3px;
          cursor: pointer;
          title='Value: ${value}'
        "></div>`;
      });
    });

    html += '</div>';
    container.innerHTML = html;
    return container;
  },

  /**
   * Create statistics cards (DOM-based)
   */
  createStatCards: function(containerId, stats) {
    const container = document.getElementById(containerId);
    if (!container) return null;

    let html = '<div class="stat-cards" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">';

    Object.entries(stats).forEach(([label, value]) => {
      html += `
        <div class="stat-card" style="
          padding: 16px;
          background: var(--card);
          border: 1px solid var(--rule);
          border-radius: 4px;
          text-align: center;
        ">
          <div style="font-size: 12px; color: var(--muted); margin-bottom: 8px;">
            ${label.replace(/_/g, ' ').toUpperCase()}
          </div>
          <div style="font-size: 24px; font-weight: 600; color: var(--ink);">
            ${typeof value === 'number' ? value.toLocaleString() : value}
          </div>
        </div>
      `;
    });

    html += '</div>';
    container.innerHTML = html;
    return container;
  },

  /**
   * Create progress bars (DOM-based)
   */
  createProgressBars: function(containerId, items) {
    const container = document.getElementById(containerId);
    if (!container) return null;

    const maxValue = Math.max(...items.map(i => i.value), 1);
    let html = '<div class="progress-bars" style="display: flex; flex-direction: column; gap: 12px;">';

    items.forEach((item) => {
      const percentage = (item.value / maxValue) * 100;
      html += `
        <div style="margin-bottom: 8px;">
          <div style="font-size: 12px; margin-bottom: 4px; display: flex; justify-content: space-between;">
            <span>${item.label}</span>
            <span>${item.value}</span>
          </div>
          <div style="
            width: 100%;
            height: 8px;
            background: var(--rule);
            border-radius: 4px;
            overflow: hidden;
          ">
            <div style="
              width: ${percentage}%;
              height: 100%;
              background: var(--accent);
              transition: width 0.3s ease;
            "></div>
          </div>
        </div>
      `;
    });

    html += '</div>';
    container.innerHTML = html;
    return container;
  },

  /**
   * Create a simple sparkline (inline mini chart)
   */
  createSparkline: function(canvasId, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    canvas.width = options.width || 100;
    canvas.height = options.height || 30;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    if (!data || data.length === 0) return canvas;

    const maxValue = Math.max(...data, 1);
    const barWidth = width / data.length;

    ctx.fillStyle = options.color || '#c8401a';

    data.forEach((value, idx) => {
      const barHeight = (value / maxValue) * height;
      const x = idx * barWidth;
      const y = height - barHeight;
      ctx.fillRect(x, y, barWidth - 1, barHeight);
    });

    return canvas;
  }
};

// Make it globally available
window.GraphRenderer = window.GraphRenderer || {};
