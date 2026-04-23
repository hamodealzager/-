const form = document.getElementById("currency-form");
const tbody = document.getElementById("currency-body");
const rowTemplate = document.getElementById("row-template");
const totalLabel = document.getElementById("total");

const portfolio = [
  { id: crypto.randomUUID(), name: "Bitcoin", symbol: "BTC", amount: 0.75, price: 64000 },
  { id: crypto.randomUUID(), name: "Ethereum", symbol: "ETH", amount: 4.5, price: 3100 }
];

const formatUsd = (value) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);

function render() {
  tbody.innerHTML = "";

  for (const currency of portfolio) {
    const row = rowTemplate.content.cloneNode(true);
    const tr = row.querySelector("tr");
    tr.dataset.id = currency.id;

    row.querySelector('[data-field="name"]').textContent = currency.name;
    row.querySelector('[data-field="symbol"]').textContent = currency.symbol;
    row.querySelector('[data-field="amount"]').value = currency.amount;
    row.querySelector('[data-field="price"]').value = currency.price;
    row.querySelector('[data-field="value"]').textContent = formatUsd(currency.amount * currency.price);

    tbody.appendChild(row);
  }

  const total = portfolio.reduce((acc, item) => acc + item.amount * item.price, 0);
  totalLabel.textContent = `إجمالي القيمة: ${formatUsd(total)}`;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const name = document.getElementById("name").value.trim();
  const symbol = document.getElementById("symbol").value.trim().toUpperCase();
  const amount = Number.parseFloat(document.getElementById("amount").value);
  const price = Number.parseFloat(document.getElementById("price").value);

  if (!name || !symbol || Number.isNaN(amount) || Number.isNaN(price)) {
    return;
  }

  portfolio.push({ id: crypto.randomUUID(), name, symbol, amount, price });
  form.reset();
  render();
});

tbody.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;

  const tr = button.closest("tr");
  const id = tr?.dataset.id;
  const index = portfolio.findIndex((item) => item.id === id);
  if (index === -1) return;

  if (button.dataset.action === "delete") {
    portfolio.splice(index, 1);
    render();
    return;
  }

  if (button.dataset.action === "save") {
    const amountInput = tr.querySelector('[data-field="amount"]');
    const priceInput = tr.querySelector('[data-field="price"]');
    const amount = Number.parseFloat(amountInput.value);
    const price = Number.parseFloat(priceInput.value);

    if (Number.isNaN(amount) || Number.isNaN(price) || amount < 0 || price < 0) {
      return;
    }

    portfolio[index].amount = amount;
    portfolio[index].price = price;
    render();
  }
});

render();
