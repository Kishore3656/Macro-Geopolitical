"""
Core UI Components - Sovereign Intelligence Framework
Reusable component library for tactical dashboards
"""

from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum
import streamlit as st


class ButtonVariant(Enum):
    PRIMARY = "btn-primary"
    SECONDARY = "btn-secondary"


class StatusLevel(Enum):
    POSITIVE = "text-positive"
    NEGATIVE = "text-negative"
    PRIMARY = "text-primary"
    NEUTRAL = "text-secondary"


@dataclass
class ButtonProps:
    label: str
    variant: ButtonVariant = ButtonVariant.PRIMARY
    disabled: bool = False
    width: str = "auto"
    on_click: Optional[Callable] = None


@dataclass
class DataPoint:
    value: str
    label: str
    status: StatusLevel = StatusLevel.NEUTRAL
    secondary: Optional[str] = None


def button(props: ButtonProps) -> bool:
    """Tactical button actuator"""
    css_class = f"btn {props.variant.value}"
    col1, col2, col3 = st.columns([1, 2, 1]) if props.width == "full" else (st.container(), None, None)

    container = col1 if props.width == "full" else st.container()

    with container:
        return st.button(
            props.label,
            disabled=props.disabled,
            key=f"btn_{props.label}",
            use_container_width=props.width == "full",
            on_click=props.on_click
        )


def input_field(
    label: str,
    placeholder: str = "",
    key: Optional[str] = None,
    value: str = ""
) -> str:
    """Terminal prompt style input"""
    return st.text_input(
        label,
        placeholder=placeholder,
        key=key or f"input_{label}",
        value=value,
    )


def data_card(
    title: str,
    data_points: List[DataPoint],
    footer: Optional[str] = None,
    expanded: bool = True
) -> None:
    """Intelligence unit data card"""
    with st.container():
        # Card header with active indicator
        with st.container():
            st.markdown(f"### {title}")

        # Card body - data points with vertical spacing
        st.divider()

        for i, point in enumerate(data_points):
            col1, col2 = st.columns([2, 3])

            with col1:
                st.markdown(f"**{point.label}**")

            with col2:
                status_class = point.status.value
                value_html = f'<span class="{status_class}">{point.value}</span>'
                st.markdown(value_html, unsafe_allow_html=True)

            if point.secondary:
                st.caption(point.secondary)

            if i < len(data_points) - 1:
                st.markdown("---")

        if footer:
            st.divider()
            st.caption(footer)


def metric_box(
    label: str,
    value: str,
    status: StatusLevel = StatusLevel.NEUTRAL,
    trend: Optional[str] = None
) -> None:
    """High-contrast metric display"""
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f'<p class="label-md">{label}</p>', unsafe_allow_html=True)

    with col2:
        if trend:
            st.markdown(f'<span class="text-secondary">{trend}</span>', unsafe_allow_html=True)

    st.markdown(f'<p class="data-lg {status.value}">{value}</p>', unsafe_allow_html=True)


def live_indicator(label: str) -> None:
    """Amber pulse live status indicator"""
    st.markdown(
        f'<div class="live-indicator">{label}</div>',
        unsafe_allow_html=True
    )


def panel_header(title: str, subtitle: Optional[str] = None) -> None:
    """Panel header with typography"""
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)


def data_grid(
    data: List[Dict[str, Any]],
    columns: int = 3,
    height: Optional[int] = None
) -> None:
    """Responsive data grid"""
    cols = st.columns(columns)

    for idx, item in enumerate(data):
        with cols[idx % columns]:
            with st.container():
                for key, value in item.items():
                    st.markdown(f"**{key}:** {value}")


def collapsible_section(
    title: str,
    content: Callable,
    initially_expanded: bool = True
) -> None:
    """Collapsible panel with hydraulic feel"""
    with st.expander(title, expanded=initially_expanded):
        content()


def status_badge(
    text: str,
    status: StatusLevel = StatusLevel.NEUTRAL
) -> None:
    """Inline status indicator"""
    st.markdown(
        f'<span class="{status.value}">{text}</span>',
        unsafe_allow_html=True
    )


def divider_section() -> None:
    """Vertical spacing divider"""
    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)


def tactical_glass_panel(content: Callable) -> None:
    """Floating tactical glass panel"""
    with st.container():
        st.markdown('<div class="tactical-glass">', unsafe_allow_html=True)
        content()
        st.markdown('</div>', unsafe_allow_html=True)


def stat_comparison(
    label: str,
    current: str,
    previous: str,
    status: StatusLevel = StatusLevel.NEUTRAL
) -> None:
    """Side-by-side metric comparison"""
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.markdown(f"**{label}**")

    with col2:
        st.markdown(f'<span class="{status.value} data-md">{current}</span>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<span class="text-secondary data-sm">{previous}</span>', unsafe_allow_html=True)


def activity_timeline(
    events: List[Dict[str, str]]
) -> None:
    """Vertical activity timeline"""
    for event in events:
        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown(f'<span class="live-indicator">{event.get("time", "")}</span>', unsafe_allow_html=True)

        with col2:
            st.markdown(f'**{event.get("title", "")}**')
            st.caption(event.get("description", ""))

        st.divider()


def data_table_tactical(
    data: List[Dict[str, Any]],
    columns: List[str]
) -> None:
    """Monospace data table with tactical styling"""
    st.dataframe(
        [
            {col: row.get(col, "-") for col in columns}
            for row in data
        ],
        use_container_width=True,
        hide_index=True
    )


def alert_box(
    message: str,
    severity: StatusLevel = StatusLevel.NEUTRAL
) -> None:
    """Alert notification box"""
    severity_class = {
        StatusLevel.POSITIVE: "bg-positive-subtle",
        StatusLevel.NEGATIVE: "bg-negative-subtle",
        StatusLevel.PRIMARY: "text-primary",
        StatusLevel.NEUTRAL: ""
    }

    css_class = severity_class.get(severity, "")
    st.markdown(
        f'<div class="{css_class} p-lg" style="border-left: 4px solid var(--color-primary);">{message}</div>',
        unsafe_allow_html=True
    )


def hero_stat(
    value: str,
    label: str,
    accent: bool = False
) -> None:
    """Large, prominent statistic display"""
    color = "var(--color-primary)" if accent else "var(--color-on-surface)"
    st.markdown(
        f'<div style="text-align: center;"><p class="data-lg" style="color: {color};">{value}</p><p class="label-md">{label}</p></div>',
        unsafe_allow_html=True
    )


def sidebar_menu(
    items: List[Dict[str, str]],
    active_key: Optional[str] = None
) -> Optional[str]:
    """Vertical sidebar navigation menu"""
    selected = None
    for item in items:
        key = item.get("key")
        label = item.get("label")
        icon = item.get("icon", "")

        is_active = key == active_key
        css_class = "text-primary" if is_active else ""

        if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True):
            selected = key

    return selected


def section_divider(text: Optional[str] = None) -> None:
    """Section separator with optional label"""
    if text:
        st.markdown(f'<p class="label-md text-secondary">{text}</p>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color: var(--color-outline-variant); border-color: rgba(83, 68, 53, 0.15);">', unsafe_allow_html=True)
    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
