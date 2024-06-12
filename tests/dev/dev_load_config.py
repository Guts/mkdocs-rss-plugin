from mkdocs.config import load_config

from mkdocs_rss_plugin.plugin import GitRssPlugin

mkdocs_cfg = load_config(config_file="tests/fixtures/mkdocs_multiple_instances.yml")

print(mkdocs_cfg.plugins.keys())
rss_instances = [
    plg for plg in mkdocs_cfg.plugins.items() if isinstance(plg[1], GitRssPlugin)
]
print(len(rss_instances))

for plg in mkdocs_cfg.plugins.items():
    print(plg)
    print(isinstance(plg[1], GitRssPlugin))
    print(type(plg))

rss_instance_1 = plg[1]
print(dir(rss_instance_1))
print(rss_instance_1.on_config(mkdocs_cfg))
