async function fetchResults() {
    const response = await fetch('/api/detection');
    const results = await response.json();
    const tableBody = document.getElementById('results-table-body');
    tableBody.innerHTML = '';
    results.slice(-15).forEach(result => { // 只顯示最新的 15 筆資料
        const row = document.createElement('tr');
        row.innerHTML = `
            <td style="color: #fff;">${result.label}</td>
            <td style="color: #fff;">${result.confidence}</td>
            <td style="color: #fff;">${result.x1}</td>
            <td style="color: #fff;">${result.y1}</td>
            <td style="color: #fff;">${result.x2}</td>
            <td style="color: #fff;">${result.y2}</td>
        `;
        tableBody.appendChild(row);
    });
}

setInterval(fetchResults, 2000); // 每5秒更新一次結果