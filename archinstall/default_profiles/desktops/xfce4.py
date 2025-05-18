from typing import override

from archinstall.default_profiles.profile import GreeterType, ProfileType
from archinstall.default_profiles.xorg import XorgProfile


class Xfce4Profile(XorgProfile):
	def __init__(self) -> None:
		super().__init__("Xfce4", ProfileType.DesktopEnv)

	@property
	@override
	def packages(self) -> list[str]:
		return [
			"base-devel",
			"btop",
			"duf",
			"firefox",
			"ghostty",
			"neovim",
			"nfs-utils",
			"xfce4-arch-boki-meta",
			"archboki-xfce",
			"archboki-shells",
			"archboki-ghostty-config",
		]

	@property
	@override
	def default_greeter_type(self) -> GreeterType:
		return GreeterType.Sddm
