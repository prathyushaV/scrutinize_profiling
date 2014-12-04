Filename:/opt/stack/new/nova/nova/api/openstack/wsgi.py
Methodname:__call__
22
           @webob.dec.wsgify(RequestClass=Request)
           @coverage
           def __call__(self, request):
               """WSGI method that controls (de)serialization and method dispatch."""
       
               # Identify the action, its arguments, and the requested
               # content type
               ###Added by Bharath
+++++++        action_args_null = self.get_action_args(request.environ)
+++++++        action_empty = action_args_null.pop('action', None)
+++++++        content_type, body = self.get_body(request)
+++++++        accept_null = request.best_match_content_type()
       
+++++++        action_args = self.get_action_args(request.environ)
+++++++        action = action_args.pop('action', None)
+++++++        content_type, body = self.get_body(request)
+++++++        accept = request.best_match_content_type()
       
               # NOTE(Vek): Splitting the function up this way allows for
               #            auditing by external tools that wrap the existing
               #            function.  If we try to audit __call__(), we can
               #            run into troubles due to the @webob.dec.wsgify()
               #            decorator.
+++++++        return self._process_stack(request, action, action_args,
+++++++                               content_type, body, accept)
