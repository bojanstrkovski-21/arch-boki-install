from typing import override

from archinstall.default_profiles.desktops import SeatAccess
from archinstall.default_profiles.profile import GreeterType, ProfileType
from archinstall.default_profiles.xorg import XorgProfile
from archinstall.lib.translationhandler import tr
from archinstall.tui.curses_menu import SelectMenu
from archinstall.tui.menu_item import MenuItem, MenuItemGroup
from archinstall.tui.result import ResultType
from archinstall.tui.types import Alignment, FrameProperties


class HyprlandProfile(XorgProfile):
	def __init__(self) -> None:
		super().__init__('Hyprland', ProfileType.DesktopEnv)

		self.custom_settings = {'seat_access': None}

	@property
	@override
	def packages(self) -> list[str]:
		return [
			'hyprland',
			'hyprpaper',
			'hyprpicker',
			'hypridle',
			'hyprlock',
			'hyprsunset',
			'hyprpolkitagent',
			'hyprshot',
			'hyprsysteminfo-git',
			'hyprland-protocols',
			'network-manager-applet'
			'nwg-look',
			'git',
			'neovim',
			'dunst',
			'kitty',
			'uwsm',
			'thunar',
			'fuzzel',
			'xdg-desktop-portal',
			'xdg-desktop-portal-gtk',
			'xdg-desktop-portal-hyprland',
			'xdg-user-dirs',
			'xdg-user-dirs-gtk',
			'qt5',
			'qt5-graphicaleffects'
			'qt6',
			'qt5-wayland',
			'qt6-wayland',
			'wlogout',
			'swww',
			'wget',
			'grim',
			'slurp',
			'yay',
			'imagemagick',
			'libsixel',
			'sublime-text-4',
			'bash-completion',
			'zoxide',
			'most',
			'fzf',
			'fish',
			'eza',
		]

	@property
	@override
	def default_greeter_type(self) -> GreeterType:
		return GreeterType.Sddm

	@property
	@override
	def services(self) -> list[str]:
		if pref := self.custom_settings.get('seat_access', None):
			return [pref]
		return []

	def _ask_seat_access(self) -> None:
		# need to activate seat service and add to seat group
		header = tr('Hyprland needs access to your seat (collection of hardware devices i.e. keyboard, mouse, etc)')
		header += '\n' + tr('Choose an option to give Hyprland access to your hardware') + '\n'

		items = [MenuItem(s.value, value=s) for s in SeatAccess]
		group = MenuItemGroup(items, sort_items=True)

		default = self.custom_settings.get('seat_access', None)
		group.set_default_by_value(default)

		result = SelectMenu[SeatAccess](
			group,
			header=header,
			allow_skip=False,
			frame=FrameProperties.min(tr('Seat access')),
			alignment=Alignment.CENTER,
		).run()

		if result.type_ == ResultType.Selection:
			self.custom_settings['seat_access'] = result.get_value().value

	@override
	def do_on_select(self) -> None:
		self._ask_seat_access()
		return None
