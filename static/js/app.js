const caughtmons = [];

const fusionBox = document.querySelector(".mons-in-box");
const clearButton = document.querySelector(".clear-box");
const clearRow = document.querySelector(".clear-row")
// button to reset each row
// update the table sprite in real time?
function renderFusionBox() {
    fusionBox.replaceChildren();

    caughtmons.forEach((name) => {
        const card = document.createElement("div");
        card.className = "caught-mon";
        const nameLabel = document.createElement("span");
        nameLabel.textContent = name;
        

        const cardImage = document.createElement("img");
        const option = Array.from(document.querySelectorAll("option"))
            .find((entry) => entry.value === name);

        if (option?.dataset.pokemonId) {
            cardImage.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${option.dataset.pokemonId}.png`;
            cardImage.alt = `${name} sprite`;

        }

        card.append(cardImage, nameLabel);
        fusionBox.append(card);
    });
}

function onClickDel(button) {
    const row = button.closest(".h-location-row");

    if (!row) {
        return;
    }

    const previousNames = row.dataset.caughtMons
        ? JSON.parse(row.dataset.caughtMons)
        : [];

    previousNames.forEach(name => {
        let index = caughtmons.indexOf(name);

        while (index !== -1) {
            caughtmons.splice(index, 1);
            index = caughtmons.indexOf(name);
        }
    });

    row.querySelectorAll(".pokemon-input").forEach(input => {
        input.value = "";
    });

    const inputsContainer = row.querySelector(".encounter-inputs");
    const inputs = inputsContainer.querySelectorAll(".encounter-input");

    if (inputs.length > 1) {
        inputs[1].remove();
    }

    row.querySelector(".fuse-button").textContent = "Fuse";
    row.querySelector(".status-select").value = "Select";
    row.dataset.caughtMons = JSON.stringify([]);

    renderRowSprites(row);
    renderFusionBox();
}

document.addEventListener("change", (event) => {
    if (!event.target.matches(".status-select")) {
        return;
    }
    

    const row = event.target.closest("tr");
    const inputs = row.querySelectorAll(".pokemon-input");
    const names = Array.from(inputs)
        .map(input => input.value.trim())
        .filter(Boolean);


    const previousNames = row.dataset.caughtMons
        ? JSON.parse(row.dataset.caughtMons)
        : [];

    previousNames.forEach(name => {
        const index = caughtmons.indexOf(name);

        if (index !== -1) {
            caughtmons.splice(index, 1);
        }
    });

    if (event.target.value === "caught") {
        names.forEach(name => {
            caughtmons.push(name);
        });
        row.dataset.caughtMons = JSON.stringify(names);
    } else {
        row.dataset.caughtMons = JSON.stringify([]);
    }

    renderFusionBox();
    });

document.addEventListener("change", (event) => {
    if (!event.target.matches(".pokemon-input")) {
        return;
    }

    const input = event.target;
    const row = input.closest("tr");
    renderRowSprites(row);
});

clearButton.addEventListener("click", () => {
    caughtmons.length = 0;
    document.querySelectorAll(".h-location-row").forEach(row => {
    row.dataset.caughtMons = JSON.stringify([]);
    });
    renderFusionBox();
});

function onClickAdd(button) {
    const container = button.closest(".encounter-container");
    const inputsContainer = container.querySelector(".encounter-inputs");
    const inputs = inputsContainer.querySelectorAll(".encounter-input");

    if (inputs.length === 1) {
        const clone = inputs[0].cloneNode(true);
        const input = clone.querySelector(".pokemon-input");
        input.value = "";
        inputsContainer.appendChild(clone);
        button.textContent = "Unfuse";
    } else {
        inputs[1].remove();
        button.textContent = "Fuse";
    }
}

function renderRowSprites(row) {
    const spritecol = row.querySelector(".spriteimg");
    const inputs = Array.from(row.querySelectorAll(".pokemon-input"));
    const names = inputs.map(input => input.value.trim()).filter(Boolean);
    const options = inputs.map(input => Array.from(document.querySelectorAll("option"))
        .find(entry => entry.value === input.value.trim()));
    const ids = options.map(option => option?.dataset.pokemonId);
    const isFusion = inputs.length === 2 && ids.every(Boolean);

    spritecol.replaceChildren();

    if (!names.length) {
        return;
    }

    const spriteimg = document.createElement("div");
    spriteimg.className = "caught-sprite";
    const spriteimgname = document.createElement("span");
    spriteimgname.textContent = names.join(" + ");
    const spriteimgimg = document.createElement("img");
    if (isFusion) {
        spriteimgimg.src = `https://ifd-spaces.sfo2.cdn.digitaloceanspaces.com/custom/${ids[0]}.${ids[1]}.png`;
        spriteimgimg.alt = `${names.join(" + ")} fused sprite`;
    } else if (ids[0]) {
        spriteimgimg.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${ids[0]}.png`;
        spriteimgimg.alt = `${names[0]} sprite`;
    }

    spriteimg.append(spriteimgimg, spriteimgname);
    spritecol.append(spriteimg);

}