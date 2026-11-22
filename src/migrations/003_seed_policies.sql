INSERT INTO tool_policy (tool_name, role, decision) VALUES
('fake_search', 'user', 'allow'),
('fake_search', 'guest', 'deny'),
('fake_weather', 'user', 'allow'),
('fake_weather', 'guest', 'require_approval'),
('fake_weather_http', 'user', 'allow'),
('fake_weather_http', 'guest', 'allow')
ON CONFLICT (tool_name, role) DO NOTHING;