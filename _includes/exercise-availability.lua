local drafts = {}

return {
  {
    Meta = function(meta)
      for _, path in ipairs(meta.drafts or {}) do
        drafts[pandoc.utils.stringify(path)] = true
      end
    end,
  },
  {
    Div = function(chapter)
      if not chapter.classes:includes("teaching-chapter") then
        return
      end

      local pending = false
      chapter = chapter:walk({
        Link = function(link)
          local path = link.target:match("^[^#]+")
          if drafts[path] then
            pending = true
            return pandoc.Span(link.content)
          end
        end,
      })

      if pending then
        chapter.classes:insert("teaching-pending")
        chapter.content:insert(2, pandoc.Plain({
          pandoc.Span(pandoc.Str("À paraître après le TD"), pandoc.Attr("", { "chapter-status" })),
        }))
      end

      return chapter
    end,
  },
}
