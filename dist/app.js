const navigation = document.querySelector("#navigation");
const menu = document.querySelector("#menu-button");
const compactViewport = matchMedia("(max-width: 820px)");

function toggleMenu(open, returnFocus = false) {
  navigation.dataset.open = String(open);
  menu.setAttribute("aria-expanded", String(open));
  menu.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  if (returnFocus) menu.focus();
}

if (menu && navigation) {
  function syncMenu() {
    toggleMenu(false);
    menu.hidden = !compactViewport.matches;
  }
  syncMenu();
  compactViewport.addEventListener("change", syncMenu);
  menu.addEventListener("click", () => toggleMenu(navigation.dataset.open !== "true"));
  navigation.addEventListener("click", event => {
    if (compactViewport.matches && event.target.closest("a")) toggleMenu(false);
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && navigation.dataset.open === "true") toggleMenu(false, true);
  });
  document.addEventListener("click", event => {
    if (navigation.dataset.open === "true" && !event.target.closest(".header")) toggleMenu(false);
  });
}

for (const button of document.querySelectorAll("[data-copy]")) {
  if (!navigator.clipboard) continue;
  button.hidden = false;
  const status = button.closest(".notice").querySelector(".status-copy");
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      status.textContent = "Address copied.";
    } catch {
      status.textContent = "Select the address and copy it manually.";
    }
  });
}

const controls = document.querySelector("#news-controls");
if (controls) {
  const filters = [...controls.querySelectorAll("[data-filter]")];
  const search = controls.querySelector("#news-search");
  const count = controls.querySelector("#story-count");
  const empty = document.querySelector("#no-stories");
  const stories = [...document.querySelectorAll(".story")].map(card => {
    const topics = card.dataset.topics.split(" ");
    const content = card.textContent.toLocaleLowerCase();
    return { card, topics, content };
  });
  let topic = "all";

  function filterStories() {
    const terms = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    let matches = 0;
    for (const { card, topics, content } of stories) {
      const visible = (topic === "all" || topics.includes(topic)) && terms.every(term => content.includes(term));
      card.hidden = !visible;
      if (visible) matches += 1;
    }
    count.textContent = `${matches} ${matches === 1 ? "story" : "stories"}`;
    empty.hidden = matches !== 0;
  }

  function selectTopic(nextTopic) {
    topic = nextTopic;
    for (const button of filters) button.setAttribute("aria-pressed", String(button.dataset.filter === topic));
    filterStories();
  }

  for (const button of filters) {
    button.addEventListener("click", () => selectTopic(button.dataset.filter));
  }
  search.addEventListener("input", filterStories);
  document.querySelector("#clear-news").addEventListener("click", () => {
    search.value = "";
    selectTopic("all");
    search.focus();
  });

  filterStories();
  controls.hidden = false;
}
