export function bindNewConversationButton({ button }) {
  if (!button || typeof button.addEventListener !== "function") {
    throw new TypeError("A clickable button is required");
  }

  // Intentionally incomplete starter implementation.
  // The shared test baseline must fail until a framework implements the behavior.
  button.addEventListener("click", function () {});
}
