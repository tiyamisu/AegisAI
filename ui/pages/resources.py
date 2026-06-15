"""
AegisAI — Resources Page
==========================
Legal rights, reporting procedures, NGO contacts, and online safety guides.
Accordion-style expandable sections.
"""
from __future__ import annotations
import customtkinter as ctk
from ui.theme import Theme


SECTIONS = [
    {
        "title": "⚖️  Legal Rights",
        "color": Theme.ACCENT,
        "items": [
            ("IPC Section 370 / 370A",
             "Defines trafficking as a cognisable, non-bailable offence. "
             "Punishable by 7–10 years rigorous imprisonment, up to life imprisonment for aggravated cases."),
            ("POCSO Act 2012",
             "Protects children from sexual exploitation. Mandatory reporting by anyone aware of an offence. "
             "Special courts for fast-track trials."),
            ("ITPA (Immoral Traffic Prevention Act)",
             "Governs prosecution of traffickers and protects victims from being treated as criminals."),
            ("Victim Compensation",
             "Under Section 357A CrPC, victims of trafficking are entitled to financial compensation "
             "from the State Victims Compensation Fund (SVCF)."),
            ("Right to Legal Aid",
             "Every victim has the right to free legal aid under the Legal Services Authorities Act, 1987. "
             "Apply at any District Legal Services Authority (DLSA)."),
        ],
    },
    {
        "title": "📝  How to Report",
        "color": Theme.WARNING,
        "items": [
            ("Report to Police",
             "Visit the nearest police station to file an FIR (First Information Report). "
             "If refused, approach the Superintendent of Police or Magistrate. FIR is free."),
            ("NHRC Anti-Trafficking Helpline",
             "Call 14433 (National Human Rights Commission). Available during working hours. "
             "File written complaints at nhrc.nic.in"),
            ("Cybercrime Portal",
             "Report online trafficking, grooming, or sextortion at cybercrime.gov.in. "
             "Helpline: 1930 (24/7). Anonymous reporting available."),
            ("Child Welfare Committee (CWC)",
             "For rescued children, approach the CWC in your district. "
             "CWC orders rehabilitation and care placement."),
            ("NHRC Online Complaint",
             "Visit nhrc.nic.in → File Complaint. Attach supporting documents. "
             "Track complaint status with case number."),
        ],
    },
    {
        "title": "🏥  NGO Support",
        "color": Theme.SUCCESS,
        "items": [
            ("International Justice Mission (IJM)",
             "Works with local law enforcement to rescue victims and provide aftercare. "
             "Website: ijm.org/india"),
            ("Prerana (Mumbai)",
             "Supports women and children victims of trafficking in Maharashtra. "
             "Contact: preranango.org"),
            ("Shakti Vahini (Delhi)",
             "Specialises in rescued victims, rehabilitation, and legal assistance. "
             "Website: shaktivahini.org"),
            ("ECPAT India",
             "Campaigns against child sex tourism and trafficking. "
             "Website: ecpatindia.com"),
            ("Childline India Foundation",
             "National helpline for children in distress: 1098 (free, 24/7). "
             "Website: childlineindia.org"),
        ],
    },
    {
        "title": "🔒  Online Safety",
        "color": Theme.TEXT_ACCENT,
        "items": [
            ("Verify Job Offers",
             "Always verify job offers via official company websites. "
             "Check employer registration on the Ministry of Labour's Shram portal."),
            ("Overseas Jobs — Emigrate Portal",
             "If offered a job abroad, verify at emigrate.gov.in. "
             "Legitimate overseas employers must register on this portal."),
            ("Social Media Safety",
             "Never share personal documents with online contacts. "
             "Be suspicious of strangers offering overnight riches or romantic relationships online."),
            ("Travel Safety",
             "Keep copies of ID documents separately from originals. "
             "Share travel plans with a trusted person. Avoid unregistered travel agents."),
            ("Digital Footprint",
             "Use strong passwords and two-factor authentication. "
             "Avoid sharing location data with unknown apps or contacts."),
        ],
    },
]


class ResourcesPage(ctk.CTkScrollableFrame):
    """Scrollable resource directory with expandable accordion section cards."""

    def __init__(self, parent) -> None:
        super().__init__(
            parent,
            fg_color=Theme.BG_DARK,
            corner_radius=0,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=Theme.ACCENT,
        )
        self.grid_columnconfigure(0, weight=1)
        self._expanded = {}
        self._build()

    def _build(self) -> None:
        # Page header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=Theme.PAD_LG,
                          pady=(Theme.PAD_LG, Theme.PAD_SM), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header_frame, text="📁  Resources & Guidance",
            font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header_frame,
            text="Legal rights, reporting procedures, NGO contacts, and safety tips",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        ).grid(row=1, column=0, pady=(3, 0), sticky="w")

        # Section count badge
        ctk.CTkLabel(
            header_frame,
            text=f"  {len(SECTIONS)} Sections  ",
            font=Theme.FONT_TINY,
            text_color=Theme.ACCENT,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_SM,
        ).grid(row=0, column=1, sticky="e", ipady=4)

        for sidx, section in enumerate(SECTIONS):
            self._make_section(section, row=sidx + 1)

        ctk.CTkFrame(self, height=Theme.PAD_LG, fg_color="transparent").grid(row=20, column=0)

    def _make_section(self, section: dict, row: int) -> None:
        color = section["color"]
        title = section["title"]
        items = section["items"]

        outer = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
        )
        outer.grid(row=row, column=0, padx=Theme.PAD_LG, pady=6, sticky="ew")
        outer.grid_columnconfigure(0, weight=1)

        # Left accent bar
        accent_bar = ctk.CTkFrame(outer, width=3, fg_color=color, corner_radius=0)
        accent_bar.grid(row=0, column=0, padx=(0, 0), pady=0, rowspan=2, sticky="ns")
        accent_bar.grid_propagate(False)

        # Section header (clickable to expand/collapse)
        header_frame = ctk.CTkFrame(outer, fg_color="transparent", cursor="hand2")
        header_frame.grid(row=0, column=1, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_lbl = ctk.CTkLabel(
            header_frame, text=title,
            font=Theme.FONT_SUBTITLE, text_color=color,
        )
        title_lbl.grid(row=0, column=0, padx=Theme.CARD_PAD, pady=Theme.PAD, sticky="w")

        # Item count
        count_lbl = ctk.CTkLabel(
            header_frame,
            text=f"  {len(items)} items  ",
            font=Theme.FONT_TINY,
            text_color=color,
            fg_color=Theme.BG_DARK,
            corner_radius=4,
        )
        count_lbl.grid(row=0, column=1, padx=(0, 8), ipady=2)

        expand_lbl = ctk.CTkLabel(
            header_frame, text="▼",
            font=("Segoe UI", 11), text_color=Theme.TEXT_MUTED,
        )
        expand_lbl.grid(row=0, column=2, padx=(0, Theme.PAD), pady=Theme.PAD)

        # Content frame (initially shown)
        content = ctk.CTkFrame(outer, fg_color="transparent")
        content.grid(row=1, column=1, padx=(Theme.CARD_PAD, Theme.CARD_PAD),
                     pady=(0, Theme.PAD_SM), sticky="ew")
        content.grid_columnconfigure(0, weight=1)
        self._expanded[id(outer)] = True

        for iidx, (item_title, item_body) in enumerate(items):
            item_row = ctk.CTkFrame(
                content,
                fg_color=Theme.BG_DARK,
                corner_radius=Theme.RADIUS_SM,
                border_width=0,
            )
            item_row.grid(row=iidx, column=0, pady=3, sticky="ew")
            item_row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                item_row, text=item_title,
                font=("Segoe UI", 11, "bold"), text_color=Theme.TEXT_PRIMARY,
                anchor="w",
            ).grid(row=0, column=0, padx=Theme.PAD, pady=(Theme.PAD_SM, 2), sticky="w")

            ctk.CTkLabel(
                item_row, text=item_body,
                font=Theme.FONT_BODY, text_color=Theme.TEXT_SECONDARY,
                wraplength=700, justify="left", anchor="w",
            ).grid(row=1, column=0, padx=Theme.PAD, pady=(0, Theme.PAD_SM), sticky="w")

        # Toggle collapse on click
        def _toggle(e, c=content, el=expand_lbl, oid=id(outer)):
            if self._expanded.get(oid, True):
                c.grid_remove()
                el.configure(text="▶")
            else:
                c.grid()
                el.configure(text="▼")
            self._expanded[oid] = not self._expanded.get(oid, True)

        header_frame.bind("<Button-1>", _toggle)
        title_lbl.bind("<Button-1>", _toggle)
        expand_lbl.bind("<Button-1>", _toggle)
        count_lbl.bind("<Button-1>", _toggle)
