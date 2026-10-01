## Ruby Rules

Append this section to the project `CLAUDE.md`.

- Use RSpec. Run tests with `bundle exec rspec`.
- Test in CI against Ruby 2.7, 3.0, 3.1, 3.2, and 3.3.
- Publish to RubyGems only when the gemspec version changes. `release.yml` does this.
- Store the RubyGems API key in the `RUBYGEMS_API_KEY` repo secret.

### RDoc Format

```ruby
##
# Short description of the class or method.
#
# @param name [Type] Description of the parameter.
# @return [Type] Description of the return value.
# @raise [ErrorClass] Description of when this error occurs.
#
# @example
#   result = method_name(arg)
#   # => expected output
```
