const { createApp } = Vue;

createApp({
  data() {
    return {
      ready: false,
      authed: false,
      webhook: false,
      password: "",
      err: "",
      busy: false,
      note: "",
      form: { name: "", url: "" },
      items: [],
      logs: [],
    };
  },
  async mounted() {
    const me = await fetch("/api/me").then((r) => r.json());
    this.authed = !!me.ok;
    this.webhook = !!me.webhook;
    if (this.authed) await this.load();
    this.ready = true;
  },
  methods: {
    async doLogin() {
      this.err = "";
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: this.password }),
      });
      const data = await res.json();
      if (!data.ok) {
        this.err = data.msg || "进不去";
        return;
      }
      this.authed = true;
      this.password = "";
      const me = await fetch("/api/me").then((r) => r.json());
      this.webhook = !!me.webhook;
      await this.load();
    },
    async doLogout() {
      await fetch("/api/logout", { method: "POST" });
      this.authed = false;
    },
    async load() {
      const res = await fetch("/api/targets");
      if (res.status === 401) {
        this.authed = false;
        return;
      }
      const data = await res.json();
      this.items = data.items || [];
      this.logs = data.logs || [];
    },
    async add() {
      const res = await fetch("/api/targets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.form),
      });
      const data = await res.json();
      if (!data.ok) {
        alert(data.msg || "没加上");
        return;
      }
      this.form = { name: "", url: "" };
      await this.load();
    },
    async remove(id) {
      await fetch("/api/targets/" + id, { method: "DELETE" });
      await this.load();
    },
    async check() {
      this.busy = true;
      this.note = "";
      try {
        const data = await fetch("/api/check", { method: "POST" }).then((r) => r.json());
        this.note = data.note || "";
        this.logs = data.logs || [];
      } finally {
        this.busy = false;
      }
    },
  },
}).mount("#app");
