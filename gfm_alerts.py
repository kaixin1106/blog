import re
from xml.etree import ElementTree as etree
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension

RE_ALERT = re.compile(r'^\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*', re.IGNORECASE)

TITLE_MAP = {
    'note': 'Note',
    'tip': 'Tip',
    'important': 'Important',
    'warning': 'Warning',
    'caution': 'Caution',
}

ICON_MAP = {
    'note': 'alert-note',
    'tip': 'alert-tip',
    'important': 'alert-important',
    'warning': 'alert-warning',
    'caution': 'alert-caution',
}

ICON_SVG = (
    '<svg class="callout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<use href="#{icon}"/></svg>'
)


class GfmAlertTreeprocessor(Treeprocessor):
    def run(self, root):
        for blockquote in root.iter('blockquote'):
            alert_p = None
            for p in blockquote:
                if p.tag != 'p' or p.text is None:
                    continue
                if RE_ALERT.match(p.text):
                    alert_p = p
                    break
            if alert_p is None:
                continue

            m = RE_ALERT.match(alert_p.text)
            alert_type = m.group(1).lower()
            blockquote.set('class', f'callout callout-{alert_type}')

            alert_p.text = RE_ALERT.sub('', alert_p.text)

            icon_svg = etree.fromstring(
                ICON_SVG.format(icon=ICON_MAP[alert_type])
            )

            title_strong = etree.Element('strong')
            title_strong.text = TITLE_MAP[alert_type]

            header_p = etree.Element('p')
            header_p.set('class', 'callout-header')
            header_p.append(icon_svg)
            header_p.append(title_strong)

            blockquote.insert(0, header_p)
        return None


class GfmAlertExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(
            GfmAlertTreeprocessor(md), 'gfm_alert', 15
        )
