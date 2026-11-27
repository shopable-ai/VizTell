import { bindNewConversationButton } from "./project-page.js";

const root = document.querySelector("[data-project-root]");
const button = document.querySelector("[data-action='new-conversation']");
const status = document.querySelector("[data-role='status']");

bindNewConversationButton({
  root,
  button,
  status,
  page: {
    href: window.location.href,
    draft: document.querySelector("textarea")?.value || "",
    scrollTop: window.scrollY
  },
  openTab: function (url) {
    window.open(url, "_blank", "noopener,noreferrer");
  }
});
